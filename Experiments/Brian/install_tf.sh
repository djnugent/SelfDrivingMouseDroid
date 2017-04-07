#!/bin/bash
sudo apt-get update
# pre req's
sudo apt-get update -qq 
	sudo apt-get --assume-yes install \
	build-essential \
	g++ \
	git \
	
	python \
	python-dev \
	python-pip \
	python-setuptools \
	python-virtualenv \
	python-wheel \
	pkg-config \

	libopenblas-base \
	python-numpy \
	python-scipy \
	
	python-h5py \
	python-yaml \
	python-pydot \

	libopencv-dev \
	python-opencv \
	python-serial
	
# for protobuf
sudo apt-get install autoconf automake libtool maven

# bazel might not need to install bazel since I built it already
sudo apt-get install pkg-config zip g++ zlib1g-dev unzip openjdk-8-jdk
# may need to do this by hand
sudo update-alternatives --config java
2
# tensorflow
sudo apt-get install python-pip python-numpy swig python-dev
sudo pip install wheel

# optimization
sudo apt-get install gcc-4.8 g++-4.8
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
