#!/bin/bash
# script to run the sudo updates

sudo apt-get update

sudo apt-get install -y \
	build-essential \
	g++ \
	git \
	curl \
	cmake \
	python3.4 \
	python3.4-pip \
	pkg-config \
	
	libopenblas-base \
	libatlas-base-dev \
	gfortran \
	python3-numpy \
	
	python3-h5py \
	python3-yaml \
	
	libopencv-dev
	
echo -e "Please restart and then run the second script\n"