#/bin/bash

# Setup prompt
export PS1="\[\033[38;5;2m\]\u\[$(tput sgr0)\]\[\033[38;5;15m\]@\h:\[$(tput sgr0)\]\[\033[38;5;11m\]\w\[$(tput sgr0)\]\[\033[38;5;15m\]\\$ \[$(tput sgr0)\]"

# Add local applications to PATH(like tmux)
PATH=$PATH:$HOME/local/bin

# Set up CUDA for tensorflow
export CUDA_INSTALL_PATH=/usr/local/cuda-8.0
export PATH=$PATH:$CUDA_INSTALL_PATH/bin/
export CUDA_HOME=$CUDA_INSTALL_PATH
export CUDA_PATH=$CUDA_INSTALL_PATH
export LD_LIBRARY_PATH=$CUDA_INSTALL_PATH/lib64
alias python='python3'
alias pip='pip3'
echo Running CUDA environment in Bash shell with Python3
