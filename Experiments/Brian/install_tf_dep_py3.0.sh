#!/bin/bash
#!/bin/bash
sudo apt-get update
# pre req's
sudo apt-get update -qq 
sudo apt-get install -y \
	build-essential \
	g++ \
	git \
	python3.0 \
	python3.0-dev \
 	python3.0-pip \
	python3.0-setuptools \
	python3.0-virtualenv \
	python3.0-wheel \
	pkg-config \

	libopenblas-base \
	python3.0-numpy \
	python3.0-scipy \
	
	python3.0-h5py \
	python3.0-yaml \
	python3.0-pydot \

	libopencv-dev \	
	python3.0-opencv \
	python3.0-serial
	
# for protobuf
sudo apt-get install autoconf automake libtool maven

# bazel might not need to install bazel since I built it already
sudo apt-get install pkg-config zip g++ zlib1g-dev unzip openjdk-8-jdk
# may need to do this by hand
sudo update-alternatives --config java
2
# tensorflow
#sudo apt-get install python-pip python-numpy swig python-dev
sudo apt-get install swig
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
