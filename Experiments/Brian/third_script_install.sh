#!/bin/bash

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

echo -e "Please restart and run the fourth install script\n"