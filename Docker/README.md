# Docker images

## Summary
Docker is a way to run software in VM that has the same environment **EVERYTIME**. It will allow us to have consistent system environments between team members, servers, and robots. This way won't have to worry about porting our code over to another system and it not working because the system configuration is different. It's one less variable to debug.

## Terminology
 **Image** - A screenshot of a system image. It usually contains an OS and preinstalled software. You can also pre load it with files but usually for development I use the file system of the host machine.

 **Container** - Is a virtual machine(VM) that runs a docker Image

 **Engine** - Docker engine is service that manages containers

 **Host** - The machine that hosts the docker VMS

## Run a Docker
 If you haven't already downloaded a docker client(engine) for you machine do so here https://docs.docker.com/engine/getstarted/step_one/

 1. Open up docker(engine) on your PC
 2. If it's your first time running an image or you have changed an image's Dockerfile then you will need to build the image. First navigate to the directory with the Dockerfile and run `docker build -t <NAME_OF_IMAGE> -f <DOCKERFILE> .` i.e. `docker build -t docker-cnn -f Dockerfile.cpu .`
 3. Run the image using ``docker run -it --rm -v `pwd`:/srv/ <NAME_OF_IMAGE>`` The `-it` flag says you want to run an interactive session with a terminal, not a background session. The `--rm` closes any existing containers using the same image. This is useful if a container require sole access to a resource i.e. GPU. The `-v` flag attaches a volume from your host machine to your docker instance. In this case it maps the directory in which you started the image in to the directory `~/srv` on the docker instance. Other useful flags are `-p` which maps ports when doing networking stuff and `--devices` which maps hardware from the host machine to docker instance i.e. webcams.
 4. Use `exit` to close the instance

## Notes
 - There is no DISPLAY object for docker instances. That means you can't run GUI applications. There are docker images that support VNC servers but that shouldn't be necessary for what we are doing. I am working on a python webserver module that will allow us to stream videos or images from python to a webpage for quick debugging.
 - When communicating over the network with a docker instance, the IP address can be found at the top of the terminal session. It gets printed once it starts. **Remember to do port mapping!!!**
 - If you install software(using apt-get, pip, etc) while an instance is running, the software will only persist for that session. Meaning next time you run the image, you will have to reinstall it. If you want new software to persist between sessions you need to modify the Dockerfile and rebuild the image.
 - In order to leverage the GPU images you must install `nvidia-docker`(this assumes you have to proper nvidia/cuda/cudnn drivers installed on the host machine) You can install `nvidia-docker` using the following command:

    `wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.0/nvidia-docker_1.0.0-1_amd64.deb && sudo dpkg -i /tmp/nvidia-docker*.deb && rm /tmp/nvidia-docker*.deb`


## Images
  - **Dockerfile.cpu** - CPU version of keras/tensorflow
  - **Dockerfile.gpu** - GPU version of keras/tensorflow with prebuilt cuda. Note: *Run `nvidia-docker` instead of `docker`*
  - **Dockerfile.cuda** - GPU version of keras/tensorflow that rebuilds cuda(slow but low dependencies) Note: *Run `nvidia-docker` instead of `docker`*
