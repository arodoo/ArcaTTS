#!/bin/bash

echo "Setting up AudioLibros TTS environment..."

# Create virtual environment
python -m venv venv

# Activate venv
source venv/Scripts/activate

# Upgrade pip
pip install --upgrade pip

# Install PyTorch with CUDA support
pip install torch torchvision torchaudio \
  --index-url https://download.pytorch.org/whl/cu121

# Install remaining dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt')"

echo "Setup complete! Activate venv: source venv/Scripts/activate"
