#!/bin/bash

# Update system packages
sudo yum update -y

# Install dependencies
sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel

# Download Python 3.12 source code
wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
tar -xf Python-3.12.0.tgz
cd Python-3.12.0

# Configure and build Python
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall

# Clean up
cd ..
rm -rf Python-3.12.0 Python-3.12.0.tgz

# Verify Python installation
python3.12 --version
