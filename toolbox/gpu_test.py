'''
====================================================================================================
Helper function for the VideoPyToolbox

MIT License Copyright (c) 2021 GuillermoHidalgoGadea.com

Sourcecode: https://github.com/Guillermo-Hidalgo-Gadea/VideoPyToolbox
====================================================================================================
'''
import os                           # paths and terminal commands
import GPUtil                       # check available GPUs
from tkinter import filedialog      # interactive interface to selet files 
from datetime import datetime       # get timestamp for filenames 


if GPUtil.getAvailable():
    print("GPU detected!")
    GPU = input("Would you like to use GPU accelerated encoding? [y/N]")


if GPU == 'y':
    print("great, using hevc_nvenc encoder")
    videofile = filedialog.askopenfilenames(title='Choose Video Files you want to compress')
    cq = input("Choose CQ [0-50]: ") or 18
    # CUDA can not use crf, only -qp
    command = f"ffmpeg -y -i {videofile[0]} -an -vcodec hevc_nvenc -preset p7 -rc vbr -cq {cq} output.mp4"
    os.system(command)
else:
    print("alright, using CPU only")
    videofile = filedialog.askopenfilenames(title='Choose Video Files you want to compress')
    crf = input("Choose constant rate factor between 0-50: ") or 18
    command = f"ffmpeg -y -i {videofile[0]} -an -vcodec libx265 -crf {crf} output2.mp4"
    os.system(command)



