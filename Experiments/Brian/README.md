# Brian's Experiments

To run a docker file
1) mount the files to a directory
	-currently there is a directory called /work
	-if there is no file do the following
	a) Make sure that the volume is shared in the virtual box shared folders (i.e. work --> D:\Documents\snrdesign)
	b) ssh into Boot2Docker VM	>> docker-machine ssh default
	C) Make a folder inside the vm  >> sudo mkdir /VM_share
	d) Mount the windows folder	>> sudo mount -t vboxsf work /VM_share
	e) Exit the Boot2Docker VM	>> exit
	f) Build the docker file e.g.	>> docker build -t docker-base -f Dockerfile.cpu .
	g) ssh into Boot2Docker VM	>> docker-machine ssh default
	h) Run the docker		>> docker run -it --volume /VM_share:/srv docker-base
