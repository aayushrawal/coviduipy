apt update
apt upgrade
apt install python3 python3-pip git cmake libusb-1.0.0-dev g++ gcc
pip3 install opencv-python==4.3.0.36 PyQt5==5.15.0 opencv-contrib-python pyserial==3.4 pyqtgraph==0.11.0 
echo "QT_X11_NO_MITSHM=1" >> /etc/environment
cd libuvc
mkdir build
cd build
cmake ..
make && sudo make install
cd ../..


