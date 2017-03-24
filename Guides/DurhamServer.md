## How to use the Durham server
The durham server contains a Titan X which is the most powerful GPU we have. Multiple users can be logged in at once however it will slow the performance of the GPU.


1. ssh into the machine `ssh net-id@du310-06.ece.iastate.edu`
  * Make sure you are on the iastate VPN if not on campus
  * Replace net-id with your id
2. Install keras/tensorflow/opencv locally run, `pip install --user opencv-python keras tensorflow-gpu`
  * Only need to install once.
3. Set up environment variable, run `source cuda_env.sh`
  * The source file can be found in this directory
4. Run your python code!!ls
5. exit the ssh session `exit`
