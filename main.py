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
BACKGROUND_FOLDER = "source-separation-output/background/"
FINAL_OUTPUT_FOLDER = "final-output/"

# Generate Background
background_mp3_files = [BACKGROUND_FOLDER + s for s in sorted(os.listdir(BACKGROUND_FOLDER))]
print(background_mp3_files)
background_mp3 = sum([audio_util.interpret_polly_output_file(fpath) for fpath in background_mp3_files])
background_mp3.export(FINAL_OUTPUT_FOLDER + "background.mp3", format="mp3")

list_of_polly_output = [POLLY_OUTPUT_FOLDER + s for s in sorted(os.listdir(POLLY_OUTPUT_FOLDER))]
vocal_mp3 = audio_util.interpret_polly_output_file(list_of_polly_output[0])
list_of_polly_output.pop(0)

for i, fpath in enumerate(list_of_polly_output):
    vocal_mp3 += audio_util.interpret_polly_output_file(fpath)

vocal_mp3.export(FINAL_OUTPUT_FOLDER + "vocals.mp3", format="mp3")
