# Phase vocoder. Stretching without changing the pitch of a .wav file

Run `./run.sh <input.wav> <output.wav> <time_stretch_ratio>` to stretch or squeeze the audio.<p>
Used modules: [numpy](https://numpy.org), [scipy](https://scipy.org)\
Algorithm used: [Guitar Pitch Shifter](https://www.guitarpitchshifter.com/algorithm.html "An algorithm used in this project")<p>
1. Create a venv by `python -m venv venv` in terminal
2. Activate it by `venv\Scripts\activate`
3. Install required modules by `pip install -Ur requirements.txt`
4. Run the bash script `run.sh` by `./run.sh <input.wav dir> <output.wav dir (the name will be assigned)> <stretch ratio r>`.\
  Where 0<r<1 - squeeze the audio, 1<=r - stretch the audio.
