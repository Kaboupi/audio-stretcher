import scipy.io
from scipy.io import wavfile
from os.path import dirname, join as pjoin
from src.crud import load_wav, analysis, phase_shift, plot_wav_freq


if __name__ == '__main__':
    samplerate, data = load_wav()