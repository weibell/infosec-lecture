#!/bin/bash

set -e

sudo apt update
sudo apt install \
	htop \
	idle3 \
	ltrace strace \
	libimage-exiftool-perl steghide \
	wxhexeditor
	
