"""
simple crud.py script
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def plot_wav_freq(samplerate: int, data: np.ndarray) -> None:

    """
    ### Отрисовывает график частоты и громкости аудиодорожки
    """
    track_count = 0
    length = data.shape[0] / samplerate
    time = np.linspace(0., length, data.shape[0])

    fig = plt.figure()
    fig.set_size_inches(10, 4)
    
    try:        
        ax1 = plt.subplot(2, 1, 1)
        plt.plot(time, data[:, 0], label="Left channel")
        
        ax2 = plt.subplot(2, 1, 2)
        plt.plot(time, data[:, 1], label="Right channel")
        
        track_count = 2
        
    except IndexError:
        plt.plot(time, data[:], label="Main channel")
        
        track_count = 1
    
    print(f'Длина аудио - {length:.3f}s\nЧисло дорожек - {track_count}')
    print(f'Частота дискретизации - {samplerate} Гц')
        
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    
    plt.show()
    

def load_wav(input_str: str, plot: bool = False) -> None:
    """
    Returns the samplerate and data of the .wav file.
    """
    samplerate, data = wavfile.read(input_str)
    
    if plot:
        plot_wav_freq(samplerate=samplerate, data=data)
        
    return samplerate, data


def save_wav(output_str: str, samplerate: int, data: np.ndarray, plot: bool = False) -> None:
    """
    Writes the new .wav file.
    """
    wavfile.write(output_str, samplerate, data)
    print(f'File successfully saved at {output_str}.')
    
    if plot:
        plot_wav_freq(samplerate=samplerate, data=data)
