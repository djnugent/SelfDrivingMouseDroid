#!/bin/bash

sudo -H pip3 install dev \
	setuptools \
	virtualenv \
	wheel \
	numpy \
	pydot \
	serial \
	cython
	
echo -e "Please Restart and then run the tensorflow install script\n"