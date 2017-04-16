#!/bin/bash

sudo apt-get update
# pre req's
#sudo apt-get update -qq 
sudo apt-get install -y \
	build-essential \
	g++ \
	git \
	python3 \
	python3-pip \
#	python3-dev \
#	python3-setuptools \
#	python3-virtualenv \
#	python3-wheel \
	pkg-config \

	libopenblas-base \
	libatlas-base-dev gfortran \
#	python3-numpy \
#	python3-scipy \
	
#	python3-h5py \
#	python3-yaml \
#	python3-pydot \

	libopencv-dev \	
#	python3-opencv \
#	python3-serial

sudo pip3 install dev \
	setuptools \ 
	virtualenv \	
	wheel \
	numpy \
	scipy \
	h5py \
	yaml \
	pydot \
	opencv \
	serial

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
pip3 install --user wheel

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
./autogen.sh
./configure
make -j 4
sudo make install
sudo ldconfig
protoc --version
cd ..

cd ..
sudo pip3 install --user tensorflow-1.0.1-cp34-cp34m-linux_armv7l.whl
pip3 uninstall mock
pip3 install --user mock
