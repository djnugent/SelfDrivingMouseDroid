#ifndef CAR_H__
#define CAR_H__


class Link{
    private:
        bool connected;
        int mode;


    public:
        void init(int pin);
        void send_debug(float val0,float val1,float val2);
        void send_channels_in();
        void send_heartbeat();
        void set_connect_callback();
        void set_disconnect_callback();
        void set_control_callback();
        void update();

};

#endif
