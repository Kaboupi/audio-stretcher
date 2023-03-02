"""
simple crud.py script
"""
from scipy.io import wavfile
from os.path import dirname, join as pjoin
import numpy as np
import matplotlib.pyplot as plt

from scipy.fft import fft
from scipy.signal.windows import hann
from typing import List, Optional

