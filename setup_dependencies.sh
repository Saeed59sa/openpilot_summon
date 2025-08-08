#!/bin/bash

echo "📦 Starting SDRaceMode dependency installation..."

sudo apt update
sudo apt install -y python3-opencv python3-pyqt5 python3-pip

pip3 install --upgrade pip
pip3 install -r requirements.txt

echo "✅ All dependencies installed successfully."
