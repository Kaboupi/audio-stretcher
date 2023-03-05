import sys
import scipy.io
from scipy.io import wavfile
from src.compute import pitchShift

# ./run.sh "C:\PythonProjects\repos\phase_vocoder\input\test_mono.wav" "C:\PythonProjects\repos\phase_vocoder\output\test_mono_output.wav" 2.56

def load_args():
    try:
        input_arg, output_arg, shift_scale = sys.argv[1:4]
        return input_arg, output_arg, abs(float(shift_scale))
    except ValueError:
        print('Incorrect number of arguments!')

if __name__ == '__main__':
    input_str, output_str, shift_scale = load_args()  # Загрузили аргументы баш скрипта
    samplerate, data = wavfile.read(input_str)  # Записали частоту дискретизации и данные в samplerate, data соответственно
    
    if shift_scale > 0 and shift_scale < 1:
        shift_scale *= -4
        
    y = pitchShift(data, step=shift_scale * 6)
    
    wavfile.write(output_str, samplerate, y)
    