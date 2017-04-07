import serial
import multiprocessing
import signal
import time
import protocol as proto


class Car():

    def __init__(self):
        # Manage our shared memory
        mgr = multiprocessing.Manager()
        self.read_lock = mgr.Lock()
        self.write_lock = mgr.Lock()
        # Holds vehicle state
        self.status = mgr.dict({'connected':False,'mode': 'connecting',\
                                    'throttle':0,'steering':0,'aux1':0,'aux2':0,\
                                    'invld_msg_id':0,'invld_val':0,'no_RC':0,'no_heartbeat':0})
        # Holds outgoing messages
        self.outgoing = mgr.Queue()

        # Callbacks for when messages come in
        self.heartbeat_callback = None
        self.channels_callback = None

        self.IO_process = None


    # Connect to the coprocessor over Serial
    # Starts a background process for handling IO
    def connect(self,port='/dev/ttyACM0', baudrate=115200):
        args = (port,baudrate,self.status,self.outgoing,self.read_lock,self.write_lock,self.heartbeat_callback,self.channels_callback)
        self.IO_process = multiprocessing.Process(target=self.process_IO,args = args)
        self.IO_process.daemon = True
        self.IO_process.start()

        time.sleep(0.5)

    # Close connection with vehicle
    def close(self):
        if self.IO_process is not None:
            self.set_mode("failsafe")
            print("Sending termination command")
            self.IO_process.terminate()
            print("Waiting for process to join...")
            self.IO_process.join()
            print("closed")

    # Set a callback_function for when we get a heartbeat message
    # MUST BE SET BEFORE CALLING connect()
    # Cant figure out how to call a member function that modifies member variables an object in another process
    def set_heartbeat_callback(callback_function):
        raise NotImplementedError()
        self.heartbeat_callback = callback_function

    # Set a callback_function for when we get a channels_in message
    # MUST BE SET BEFORE CALLING connect()
    # Cant figure out how to call a member function that modifies member variables an object in another process
    def set_channels_callback(callback_function):
        raise NotImplementedError()
        self.channels_callback = callback_function

    # Control the vehicle's motors
    def control(self,throttle = 1500, steering=1500,aux1=1500,aux2=1500):
        msg = proto.pack_control(throttle,steering,aux1,aux2)
        with self.write_lock:
            self.outgoing.put(msg)

    # Set the vehicle's mode
    def set_mode(self,mode):
        msg = proto.pack_set_mode(mode)
        with self.write_lock:
            self.outgoing.put(msg)

    # Get the channels from the receiver
    @property
    def channels_in(self):
        with self.read_lock:
            return {k:self.status[k] for k in ["throttle","steering","aux1","aux2"] if k in self.status}

    # Get the connection status of the vehicle
    @property
    def connected(self):
        with self.read_lock:
            return self.status['connected']

    # Get the vehicle's mode
    @property
    def mode(self):
        with self.read_lock:
            return self.status['mode']

    # Get the vehicle errors
    @property
    def errors(self):
        with self.read_lock:
            return {k:self.status[k] for k in ['invld_msg_id','invld_val','no_RC','no_heartbeat'] if k in self.status}

    # I/O thread: runs in background and handles serial connection
    def process_IO(self,port,baudrate,status,outgoing,read_lock,write_lock,heartbeat_callback,channels_callback):
        #connection state
        last_heartbeat_send = 0
        last_heartbeat_recv = 0
        running = True

        # setup process to handle termination signal gracefully
        def handler(signum, frame):
            global running
            running = False
            print('process terminating....')
        signal.signal(signal.SIGTERM, handler)

        # connect over serial
        ser = None
        try:
            ser = serial.Serial(port = port, baudrate = baudrate, timeout = 0.5)
        except OSError:
            print("Unable to connect to {}".format(port))
            return

        # clear I/O buffers
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        time.sleep(0.3)

        # Main loop
        while running:
            time.sleep(0.001)

            # send heartbeat
            if(time.time() - last_heartbeat_send > 1.0/proto.HEARTBEAT_RATE):
                msg = proto.pack_heartbeat()
                ser.write(msg)
                last_heartbeat_send = time.time()

            # check for timeout
            if(time.time() - last_heartbeat_recv > proto.HEARTBEAT_TIMEOUT):
                with read_lock:
                    status['connected'] = False

            # check for outgoing messages
            with write_lock:
                if not outgoing.empty():
                    while not outgoing.empty():
                        msg = outgoing.get(block = False)
                        #print("sent",msg,len(msg))
                        ser.write(msg)
                    ser.flush()

            # check for incoming messages
            if ser.in_waiting > 0 and ser.read(1)[0] == proto.START:
                # read msg_id
                msg_id = ser.read(1)[0]
                # read payload
                payload = ser.read(proto.msg_len[msg_id])
                #print("recv",msg_id,payload)
                #decode the msg
                msg = proto.decode(msg_id,payload)

                #handle the msg
                if msg['id'] == 'heartbeat':
                    last_heartbeat_recv = time.time()
                    msg.pop('id')
                    #update car status
                    with read_lock:
                        status['connected'] = True
                        status.update(msg)
                    #call heartbeat_callback
                    if heartbeat_callback is not None:
                        pass

                elif msg['id'] == 'channels_in':
                    msg.pop('id')
                    # update car status
                    with read_lock:
                        status.update(msg)
                    # call channels_callback
                    if channels_callback is not None:
                        pass

                elif msg['id'] == 'debug':
                    print("DEBUG: {}, {}, {}".format(msg['val0'],msg['val1'],msg['val2']))

        # Exitting
        # Flush outgoing messages
        with write_lock:
            if not outgoing.empty():
                while not outgoing.empty():
                    msg = outgoing.get(block = False)
                    ser.write(msg)
                ser.flush()
        #Close serial
        ser.close()
