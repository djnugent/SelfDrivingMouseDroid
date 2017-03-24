if [$SHELL == '/bin/tscp']
then
	echo Setting up CUDA environment for TSCP shell with Python3
	setenv CUDA_INSTALL_PATH /usr/local/cuda
	setenv PATH ${PATH}:${CUDA_INSTALL_PATH}/bin/
	setenv CUDA_HOME ${CUDA_INSTALL_PATH}
	setenv CUDA_PATH ${CUDA_INSTALL_PATH}
	setenv LD_LIBRARY_PATH ${CUDA_INSTALL_PATH}/lib64
	alias python python3
	echo Done!
elif [$SHELL == '/bin/bash']
	echo Setting up CUDA environment for Bash shell with Python3
	export CUDA_INSTALL_PATH=/usr/local/cuda
	export PATH=$PATH:$CUDA_INSTALL_PATH/bin/
	export CUDA_HOME=$CUDA_INSTALL_PATH
	export CUDA_PATH=$CUDA_INSTALL_PATH
	export LD_LIBRARY_PATH=$CUDA_INSTALL_PATH/lib64
	alias python='python3'
	echo Done!
else
	echo Shell environment not recognized. Cant setup CUDA
fi
