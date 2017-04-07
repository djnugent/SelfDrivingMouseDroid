echo Setting up CUDA environment for Bash shell with Python3
export CUDA_INSTALL_PATH=/usr/local/cuda
export PATH=$PATH:$CUDA_INSTALL_PATH/bin/
export CUDA_HOME=$CUDA_INSTALL_PATH
export CUDA_PATH=$CUDA_INSTALL_PATH
export LD_LIBRARY_PATH=$CUDA_INSTALL_PATH/lib64
alias python='python3'
echo Done!
