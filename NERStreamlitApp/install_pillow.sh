#!/bin/bash

# Script to install Pillow with necessary dependencies in Streamlit Cloud

# Exit on error
set -e

# Output commands as they're executed
set -x

# Install necessary system dependencies
apt-get update -y
apt-get install -y --no-install-recommends \
  zlib1g-dev \
  libjpeg-dev \
  libpng-dev \
  libtiff-dev \
  libfreetype6-dev \
  liblcms2-dev \
  libwebp-dev

# Clean up apt cache
apt-get clean
rm -rf /var/lib/apt/lists/*

# Install Pillow
pip install --no-cache-dir pillow>=10.0.0

echo "Pillow installation complete!" 