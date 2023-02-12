'''
====================================================================================================
Helper function for the VideoPyToolbox

MIT License Copyright (c) 2022 GuillermoHidalgoGadea.com

Sourcecode: https://github.com/Guillermo-Hidalgo-Gadea/VideoPyToolbox
====================================================================================================
'''

import os
from tkinter import filedialog

def mosaic_video():
    '''
    Create Mosaic Videos
    '''
    # Choose Video File from Dialog Box
    videofiles = list(filedialog.askopenfilenames(title='Choose the Video Files to combine'))
    if not videofiles:
        return

    outputdir = filedialog.askdirectory(title='Choose Output Directory for Compression')
    if not outputdir:
        print('Please select a valid output directory')
        secondtry = filedialog.askdirectory(title='Choose Output Directory for Concatenation')
        if not secondtry:
            return
        else:
            outputdir = secondtry

    output = os.path.join(outputdir, 'mosaic_' + os.path.basename(videofiles[0]).split('.')[0])

    if len(videofiles) == 2:
        ffmpeg_command = f'ffmpeg -i {videofiles[0]} -i {videofiles[1]} -filter_complex "[0:v][1:v]hstack=inputs=2[v];[v]scale=w=1440:h=-1[scaled]" -map "[scaled]" {output}.mp4'
        os.system(ffmpeg_command)

    elif len(videofiles) == 3:
        ffmpeg_command = f'ffmpeg -i {videofiles[0]} -i {videofiles[1]} -i {videofiles[2]} -filter_complex "[0:v][1:v][2:v]hstack=inputs=3[v];[v]scale=w=1440:h=-1[scaled]" -map "[scaled]" {output}.mp4'
        os.system(ffmpeg_command)

    elif len(videofiles) == 4:
        ffmpeg_command = f'ffmpeg -i {videofiles[0]} -i {videofiles[1]} -i {videofiles[2]} -i {videofiles[3]} -filter_complex ' \
        f'"[0:v][1:v]hstack=inputs=2[top];[2:v][3:v]hstack=inputs=2[bottom];[top][bottom]vstack=inputs=2[v];[v]scale=w=1440:h=-1[scaled]" -map "[scaled]" {output}.mp4'
        os.system(ffmpeg_command)

    elif len(videofiles) == 6:
        ffmpeg_command = f'ffmpeg '\
        f'-i {videofiles[0]} -i {videofiles[1]} -i {videofiles[2]} -i {videofiles[3]} -i {videofiles[4]} -i {videofiles[5]} '\
        f'-filter_complex "[0:v][1:v][2:v]hstack=inputs=3[top];[3:v][4:v][5:v]hstack=inputs=3[bottom];[top][bottom]vstack=inputs=2[v];[v]scale=w=1440:h=-1[scaled]" -map "[scaled]" {output}.mp4'
        os.system(ffmpeg_command)

    elif len(videofiles) == 8:
        ffmpeg_command = f'ffmpeg '\
        f'-i {videofiles[0]} -i {videofiles[1]} -i {videofiles[2]} -i {videofiles[3]} -i {videofiles[4]} -i {videofiles[5]} -i {videofiles[6]} -i {videofiles[7]} '\
        f'-filter_complex "[0:v][1:v][2:v][3:v]hstack=inputs=4[top];[4:v][5:v][6:v][7:v]hstack=inputs=4[bottom];[top][bottom]vstack=inputs=2[v];[v]scale=w=1440:h=-1[scaled]" -map "[scaled]" {output}.mp4'
        os.system(ffmpeg_command)

    else:
        print("Invalid number of videos! (valid: 2, 3, 4, 6 or 8")
