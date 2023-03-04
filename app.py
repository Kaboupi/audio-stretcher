import sys
import scipy.io
from scipy.io import wavfile
from os.path import dirname, join as pjoin
from src.crud import load_wav, save_wav, plot_wav_freq
from src.compute import analysis, phase_shift, synthesation, set_params

# ./run.sh "C:\PythonProjects\repos\phase_vocoder\input\test_mono.wav" "C:\PythonProjects\repos\phase_vocoder\output\test_mono_output.wav" 2.56

def load_args():
    try:
        input_arg, output_arg, shift_scale = sys.argv[1:4]
        return input_arg, output_arg, float(shift_scale)
    except ValueError:
        print('Incorrect number of arguments!')

if __name__ == '__main__':
    input_str, output_str, shift_scale = load_args()  # Загрузили аргументы баш скрипта
    samplerate, data = load_wav(input_str)  # Записали частоту дискретизации и данные в samplerate, data соответственно
    
    set_params(frame_size=int(data.shape[0] // 1000))
    
    spectrum, frequencies = analysis(data, samplerate)  # Спектр распределения аудиочастот и на каждый тик
    phase = phase_shift(data=spectrum, samplerate=samplerate, frequencies=frequencies)  # Сдвинутые на 1 фазу значения (не нормализованные)
    
    y_n = synthesation(data=phase, frequencies=frequencies)  # TODO ДОЛЖЕН БЫТЬ ИТОГОВЫЙ ФРЕЙМ
    
    
    save_wav(output_str=output_str, samplerate=int(samplerate * shift_scale), data=data[:5*samplerate])
    