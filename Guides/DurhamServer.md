## How to use the Durham server
The durham server contains a Titan X which is the most powerful GPU we have. Multiple users can be logged in at once however it will slow the performance of the GPU.


1. ssh into the machine `ssh -t net-id@du310-06.ece.iastate.edu /bin/bash`
  * Make sure you are on the iastate VPN if not on campus
  * Replace net-id with your id
2. Install keras/tensorflow/opencv/flask and more locally run, `pip3 install --user flask h5py imageio requests opencv-python==3.1.0 keras==1.2.2 tensorflow-gpu==1.0.1`
  * Only need to install once.
3. Install tmux, `wget -O - https://gist.githubusercontent.com/djnugent/33a263f8d4139a14bad83105ea9f75b4/raw/651e5848e1eb9db3d93968cf5131827c448b0b83/install_tmux.sh | bash -e`
  * Only need to install once.
4. Set up environment for CUDA. Add the `.bashrc` file(Found in this directory) to your linux home directory
  * Only need to run once
  * WARNING: THIS WILL OVERWRITE YOUR `.bashrc`
5. Run your python code!!
6. exit the ssh session `exit`
