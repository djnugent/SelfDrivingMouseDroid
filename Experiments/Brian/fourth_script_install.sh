#!/bin/bash

#cd ..
# sudo apt-get install python3.4-dev
# pip install numpy

# mkdir opencv_tmp
 # cd opencv_tmp
 # git clone https://github.com/Itseez/opencv.git
 # cd opencv
 # git checkout 3.1.0

 # cd ..
 # mkdir opencv_contrib_tmp
 # cd opencv_contrib_tmp
 # git clone https://github.com/Itseez/opencv_contrib.git
 # cd opencv_contrib
 # git checkout 3.1.0
 # cd ..

 
 cd opencv_tmp/opencv
 pwd
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
 
 echo -e "Please make sure you test the install\n"