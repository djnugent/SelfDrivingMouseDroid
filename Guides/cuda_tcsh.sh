echo Setting up CUDA environment for TSCP shell with Python3
setenv CUDA_INSTALL_PATH /usr/local/cuda
setenv PATH ${PATH}:${CUDA_INSTALL_PATH}/bin/
setenv CUDA_HOME ${CUDA_INSTALL_PATH}
setenv CUDA_PATH ${CUDA_INSTALL_PATH}
setenv LD_LIBRARY_PATH ${CUDA_INSTALL_PATH}/lib64
alias python python3
echo Done!
