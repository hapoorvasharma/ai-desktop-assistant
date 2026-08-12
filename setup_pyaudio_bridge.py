"""
PyAudioWPatch installs itself as 'pyaudiowpatch', but SpeechRecognition
expects a module literally named 'pyaudio'. This script creates a small
bridge file so 'import pyaudio' works correctly.

Run this once after setting up a fresh virtual environment:
    python setup_pyaudio_bridge.py
"""

import pyaudiowpatch
import os

site_packages_dir = os.path.dirname(os.path.dirname(pyaudiowpatch.__file__))
bridge_path = os.path.join(site_packages_dir, "pyaudio.py")

with open(bridge_path, "w") as f:
    f.write("from pyaudiowpatch import *\n")

print(f"Created pyaudio bridge at: {bridge_path}")