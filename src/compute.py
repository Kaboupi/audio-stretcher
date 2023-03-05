import numpy as np
from scipy.fft import fft, ifft
from scipy.signal.windows import hann
from scipy.interpolate import interp1d

def createFrames(x: np.ndarray, hop_size: int = 256, frame_size: int = 1024):
    number_slices = (x.shape[0] - frame_size) // hop_size
    x = x[:int((number_slices * hop_size + frame_size))]
    
    vector_frames = np.zeros((int(x.shape[0] / hop_size), frame_size))
    
    for i in range(1, number_slices):
        idx_begin = (i - 1) * hop_size
        idx_end = (i - 1) * hop_size + frame_size
        
        vector_frames[i,:] = x[idx_begin:idx_end]
    
    return vector_frames, number_slices


def fusionFrames(frame_matrix, hop_size: int = 256):
    number_frames, size_frames = frame_matrix.shape
    
    vectorTime = np.zeros(number_frames * hop_size - hop_size + size_frames)
    timeIndex = 0
    
    for i in range(number_frames):
        vectorTime[timeIndex:timeIndex + size_frames] += frame_matrix[i,:]
        timeIndex += hop_size
        
    return vectorTime


def pitchShift(data: np.ndarray, frame_size: int = 1024, hop_size: int = 256, step: int = 2) -> np.ndarray:
    alpha = np.power(2, step / 12)
    
    hopOut = np.round(alpha * hop_size)
    wn = hann(frame_size*2 + 1)[2::2]
    
    # Source file
    data = np.concatenate([np.zeros(hop_size * 3), data])
    
    #
    y, numberFramesInput = createFrames(data)
    numberFramesOutput = numberFramesInput
    outputy = np.zeros((numberFramesOutput, frame_size))
    
    phaseCumulative = 0
    previousPhase = 0
    
    for i in range(numberFramesInput):
        
        currentFrame = y[i,:]
        currentFrameWindowed = currentFrame * wn / np.sqrt((frame_size / hop_size) / 2)
        currentFrameWindowedFFT = fft(currentFrameWindowed)
        magFrame = np.abs(currentFrameWindowedFFT)
        phaseFrame = np.angle(currentFrameWindowedFFT)
        
        # Обработка
        deltaPhi = phaseFrame - previousPhase
        previousPhase = phaseFrame
        
        deltaPhiPrime = deltaPhi - hop_size * 2 * np.pi * np.arange(frame_size) / frame_size
        deltaPhiPrimeMod = np.mod((deltaPhiPrime + np.pi), (2 * np.pi)) - np.pi
        
        trueFreq = 2 * np.pi * np.arange(frame_size) / frame_size + deltaPhiPrimeMod / hop_size
        phaseCumulative += hopOut * trueFreq
        
        # Синтез
        outputMag = magFrame
        outputFrame = np.real(ifft(outputMag * np.exp(1j * phaseCumulative)))
        
        outputy[i,:] = outputFrame * wn / np.sqrt((frame_size / hopOut) / 2)
    
    return fusionFrames(outputy, int(hopOut)).astype(np.int16)
