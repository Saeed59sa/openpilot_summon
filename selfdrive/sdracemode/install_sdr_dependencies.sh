#!/bin/bash
set -e

echo "🧠 SDRaceMode: Smart Dependency Installer Starting..."

# List of required APT packages
APT_PACKAGES=(python3-opencv python3-pyqt5 python3-pip ffmpeg)

for pkg in "${APT_PACKAGES[@]}"; do
  if ! dpkg -s "$pkg" &> /dev/null; then
    echo "📦 Installing missing system package: $pkg"
    sudo apt install -y "$pkg"
  else
    echo "✅ System package $pkg is already installed."
  fi
done

# Upgrade pip
pip3 install --upgrade pip

# List of required Python packages
PYTHON_PACKAGES=(numpy sounddevice scipy PyYAML)

for pkg in "${PYTHON_PACKAGES[@]}"; do
  if ! python3 -c "import $pkg" &> /dev/null; then
    echo "📦 Installing missing Python module: $pkg"
    pip3 install "$pkg"
  else
    echo "✅ Python module $pkg is already available."
  fi
done

echo "🎉 All SDRaceMode dependencies are now installed and ready to use."
