#!/bin/bash

sudo apt-get update
# pre req's
#sudo apt-get update -qq 
sudo apt-get install -y \
	build-essential \
	g++ \
	git \
	curl \
	python3 \
	python3-pip \
#	python3-dev \
#	python3-setuptools \
#	python3-virtualenv \
#	python3-wheel \ #
	pkg-config \

	libopenblas-base \
	libatlas-base-dev \
	gfortran \
	python3-numpy \
#	python3-scipy \
	
	python3-h5py \
	python3-yaml \
#	python3-pydot \

	libopencv-dev \	
#	python3-opencv \
#	python3-serial

## RESTART OR BREAK SCRIPT ##

sudo -H pip3 install dev \
	setuptools \ 
	virtualenv \	
	wheel \
	numpy \
#	scipy \
#	h5py \
#	yaml \#
	pydot \
#	opencv \#
	serial \
	cython		#	used for building wheels from source

# for protobuf
sudo apt-get install -y autoconf automake libtool maven

# bazel might not need to install bazel since I built it already
sudo apt-get install -y pkg-config zip g++ zlib1g-dev unzip openjdk-8-jdk
# may need to do this by hand
sudo update-alternatives --config java
2
# tensorflow
#sudo apt-get install python-pip python-numpy swig python-dev
sudo apt-get install -y swig
#pip3 install --user wheel

# optimization
sudo apt-get install -y gcc-4.8 g++-4.8
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 100
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.8 100

mkdir tf
cd tf

# build protobuf
git clone https://github.com/google/protobuf.git

cd protobuf
git checkout v3.1.0
bash autogen.sh
bash configure
make -j 4
sudo make install
sudo ldconfig
protoc --version
cd ..

#	Install scipy from source
git clone https://github.com/scipy/scipy.git

cd scipy
git clean -xdf
python3 setup.py install --user

cd ..
sudo -H pip3 install --user tensorflow-1.0.1-cp34-cp34m-linux_armv7l.whl
pip3 uninstall mock
pip3 install --user mock

cd ..
sudo apt-get install python3.4-dev
pip install numpy

mkdir opencv_tmp
 cd opencv_tmp
 git clone https://github.com/Itseez/opencv.git
 cd opencv
 git checkout 3.1.0

 cd ..
 mkdir opencv_contrib_tmp
 cd opencv_contrib_tmp
 git clone https://github.com/Itseez/opencv_contrib.git
 cd opencv_contrib
 git checkout 3.1.0
 cd ..

 
 cd opencv_tmp/opencv
 mkdir build 
 cd build
 cmake -D CMAKE_BUILD_TYPE=RELEASE 
       -D CMAKE_INSTALL_PREVIX=/usr/local
       -D INSTALL_C_EXAMPLES=OFF
       -D INSTALL_PYTHON_EXAMPLES=ON
       -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib_tmp/opencv_contrib/modlules
       -D BUILD_EXAMPLES=ON ..

 make -j4

 sudo make install
 sudo ldconfig
