import numpy as np
from scipy.fft import fft
from scipy.signal.windows import hann
from typing import List, Optional

FRAME_SIZE = 1000
OVERLAP = 0.75
HOP_A = int(FRAME_SIZE - (FRAME_SIZE * OVERLAP))

def set_params(frame_size: int, overlap: Optional[float] = 0.75):
    FRAME_SIZE = frame_size
    OVELRAP = overlap
    HOP_A = int(FRAME_SIZE - (FRAME_SIZE * OVERLAP))

# 1st ANALYSIS
def analysis(data: np.ndarray,
             samplerate: int,
             frame_size: int = FRAME_SIZE,
             overlap: float = OVERLAP,
             ) -> List[np.ndarray]:
    """
    Compute the discrete spectrum of a signal.

    Args:
        data: numpy array of shape (n,)
            The input signal to compute the spectrum for.
        frame_size: int, optional (default=n//1000)
            The size of each frame, in samples.
        overlap: float, optional (default=0.75)
            The overlap (hop size) of frames.

    Returns:
        spectrum: list of numpy arrays shaped (frame_size,)
            The spectral amplitude at each frequency bin for each frame.
    """
    hop_size = int(frame_size - (frame_size * overlap))
    num_frames = 1 + (data.shape[0] - frame_size) // hop_size
    hann_window = hann(frame_size)
    spectrum = np.zeros((frame_size // 2 + 1, num_frames))
    
    for i in range(num_frames):
        frame = data[i*hop_size:i*hop_size+frame_size] * hann_window
        spectrum[:, i] = (np.abs(fft(frame)[:frame_size // 2 + 1]))
        
    frequencies = np.fft.fftfreq(frame_size, 1/samplerate)[:frame_size//2 + 1]
        
    return spectrum, frequencies

# 2nd PHASE SHIFT
def phase_shift(data: np.ndarray,
                samplerate: int,
                frequencies: np.ndarray,
                frame_size: int = FRAME_SIZE,
                hop_size: int = HOP_A,
                ) -> np.ndarray:
    """
    Compute phase shift.
    """
    num_frames = data.shape[1]
    w_true = w_freq = w_wrapped = np.zeros((frame_size // 2 + 1, num_frames))
    
    for i in range(1, num_frames):
        w_freq[:, i-1] = (data[:, i] - data[:, i-1]) / (hop_size / samplerate) - frequencies
        w_wrapped[:, i-1] = (w_freq[:, i-1] + np.pi) % (2 * np.pi) - np.pi
        w_true[:, i-1] = w_wrapped[:, i-1] + frequencies
        
    phase = np.zeros((frame_size // 2 + 1, num_frames))
    hop_s = int(data.shape[0] - (data.shape[0] * OVERLAP))
    for i in range(1, num_frames):
        phase[:, i] = data[:, i-1] + (hop_s / samplerate) * w_true[:, i]

    return phase


# 3rd SYNTHESIS
def synthesation(data: np.ndarray,
                 frequencies: np.ndarray,
                 frame_size: int = FRAME_SIZE,
                 hop_size: int = HOP_A
                 ) -> None:
    """
    ???
    """
    hop_s = int(data.shape[0] - (data.shape[0] * OVERLAP))
    num_frames = data.shape[1]
    hann_window = hann(data.shape[0])
    Q_i = np.zeros((data.shape[0], num_frames))
    
    # for i in range(num_frames):
    #     Q_i[:, i] = np.mean(fft(np.abs(data[:, i]))) * hann_window
        
    res = np.zeros((data.shape[0], num_frames))
        
    return res
        
    # frame = data[i*hop_size:i*hop_size+frame_size] * hann_window