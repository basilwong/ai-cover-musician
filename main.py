"""
Creates the final version of the mp3 using the output of the main.ipynb
notebook.


"""


import os
import pydub

# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.append('src')

import audio_util

POLLY_OUTPUT_FOLDER = "polly-output/"
FINAL_OUTPUT_FOLDER = "final-output/"

# Generate Background

list_of_polly_output = [POLLY_OUTPUT_FOLDER + s for s in sorted(os.listdir('polly-output/'))]
vocal_mp3 = audio_util.interpret_polly_output_file(list_of_polly_output[0])
list_of_polly_output.pop(0)

for i, fpath in enumerate(list_of_polly_output):
    vocal_mp3 += audio_util.interpret_polly_output_file(fpath)

vocal_mp3.export(FINAL_OUTPUT_FOLDER + "vocals.mp3", format="mp3")
