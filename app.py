import sys
import scipy.io
from scipy.io import wavfile
from src.compute import pitchShift
import numpy as np

# ./run.sh "C:\PythonProjects\repos\phase_vocoder\input\test_mono.wav" "C:\PythonProjects\repos\phase_vocoder\output\test_mono_output.wav" 2.56
# ./run.sh "C:\PythonProjects\repos\phase_vocoder\input\test_stereo.wav" "C:\PythonProjects\repos\phase_vocoder\output\test_stereo_output.wav" 2
def load_args():
    try:
        input_arg, output_arg, shift_scale = sys.argv[1:4]
        return input_arg, output_arg, abs(float(shift_scale))
    except ValueError:
        print('Incorrect number of arguments!')

if __name__ == '__main__':
    input_str, output_str, shift_scale = load_args()  # Загрузили аргументы баш скрипта
    if shift_scale > 0 and shift_scale < 1:
        shift_scale = -1 / shift_scale
    shift_scale *= 6
    
    samplerate, data = wavfile.read(input_str)  # Записали частоту дискретизации и данные в samplerate, data соответственно
    
    try:
        y_left = pitchShift(data[:,0], step=shift_scale)
        y_right = pitchShift(data[:,1], step=shift_scale)
        y = np.array([y_left, y_right]).T
    except IndexError:
        y = pitchShift(data, step=shift_scale)
    
    wavfile.write(output_str, samplerate, y)
