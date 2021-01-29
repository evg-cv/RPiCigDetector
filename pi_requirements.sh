#!/bin/bash

echo "Installing Kivy on RPi"
sudo apt install -y libfreetype6-dev libgl1-mesa-dev libgles2-mesa-dev libdrm-dev libgbm-dev \
      libudev-dev libasound2-dev liblzma-dev libjpeg-dev libtiff-dev libwebp-dev git build-essential
sudo apt install -y gir1.2-ibus-1.0 libdbus-1-dev libegl1-mesa-dev libibus-1.0-5 libibus-1.0-dev \
      libice-dev libsm-dev libsndio-dev libwayland-bin libwayland-dev libxi-dev libxinerama-dev \
      libxkbcommon-dev libxrandr-dev libxss-dev libxt-dev libxv-dev x11proto-randr-dev \
      x11proto-scrnsaver-dev x11proto-video-dev x11proto-xinerama-dev

# Install SDL2
cd /tmp
wget https://libsdl.org/release/SDL2-2.0.10.tar.gz
tar -zxvf SDL2-2.0.10.tar.gz
pushd SDL2-2.0.10
./configure --enable-video-kmsdrm --disable-video-opengl --disable-video-x11 --disable-video-rpi
make -j$(nproc)
sudo make install
popd

# Install SDL2_image
cd /tmp
wget https://libsdl.org/projects/SDL_image/release/SDL2_image-2.0.5.tar.gz
tar -zxvf SDL2_image-2.0.5.tar.gz
pushd SDL2_image-2.0.5
./configure
make -j$(nproc)
sudo make install
popd

# Install SDL2_mixer
cd /tmp
wget https://libsdl.org/projects/SDL_mixer/release/SDL2_mixer-2.0.4.tar.gz
tar -zxvf SDL2_mixer-2.0.4.tar.gz
pushd SDL2_mixer-2.0.4
./configure
make -j$(nproc)
sudo make install
popd

# Install SDL2_ttf
cd /tmp
wget https://libsdl.org/projects/SDL_ttf/release/SDL2_ttf-2.0.15.tar.gz
tar -zxvf SDL2_ttf-2.0.15.tar.gz
pushd SDL2_ttf-2.0.15
./configure
make -j$(nproc)
sudo make install
popd

sudo ldconfig -v
sudo adduser "$USER" render
sudo adduser "root" render
sudo apt -f install
sudo apt install -y pkg-config libgl1-mesa-dev libgles2-mesa-dev python3-setuptools libgstreamer1.0-dev git-core \
    gstreamer1.0-plugins-{bad,base,good,ugly} gstreamer1.0-{omx,alsa} python3-dev python3-pip libmtdev-dev xclip xsel libjpeg-dev libilmbase-dev libopenexr-dev libgstreamer1.0-dev
sudo apt install python3-sdl2

sudo python3 -m pip install -U pip
sudo python3 -m pip install -U setuptools
sudo python3 -m pip install -U Cython pillow
sudo python3 -m pip install https://github.com/kivy/kivy/archive/master.zip
#sudo echo "gpu_mem=1024" | sudo tee -a /boot/config.txt

# Get packages required for OpenCV
sudo apt-get -y install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get -y install libxvidcore-dev libx264-dev
sudo apt-get -y install qt4-dev-tools libatlas-base-dev

# Install Coral board
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install libedgetpu1-std

# Install Maria DB
sudo apt update
sudo apt upgrade
sudo apt install -y mariadb-server

# Need to get an older version of OpenCV because version 4 has errors
pip3 install opencv-python==3.4.6.27
pip3 install mysql.connector

# Get packages required for TensorFlow
# Using the tflite_runtime packages available at https://www.tensorflow.org/lite/guide/python
# Will change to just 'pip3 install tensorflow' once newer versions of TF are added to piwheels

#pip3 install tensorflow

version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')

if [ "$version" == "3.7" ]; then
pip3 install https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.5.0-cp37-cp37m-linux_armv7l.whl
fi

if [ "$version" == "3.5" ]; then
pip3 install https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.5.0-cp35-cp35m-linux_armv7l.whl
fi