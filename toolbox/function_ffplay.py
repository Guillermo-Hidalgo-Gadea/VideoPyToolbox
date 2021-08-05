'''
====================================================================================================
Helper function for the VideoPyToolbox

MIT License Copyright (c) 2021 GuillermoHidalgoGadea.com

Sourcecode: https://github.com/Guillermo-Hidalgo-Gadea/VideoPyToolbox
====================================================================================================
'''

import os
from tkinter import filedialog

def ffplay():
    '''
    Video player with ffplay instead of OpenCV
    '''
    # Choose Video File from Dialog Box
    videofile = filedialog.askopenfilenames(title='Choose the Video Files you want to play')
    video = videofile[0]

    ffplay_timecode = "\"drawtext=fontfile=Arial.ttf: text='%{pts\:hms} Frame\: %{frame_num}': x=(w-tw)/1.1: y=h-(2*lh): fontcolor=black: fontsize=50: box=1: boxcolor=white: boxborderw=5\""
    ffplay_command = f"ffplay -x 1000 -vf {ffplay_timecode} {video}"

    os.system(ffplay_command)