'''
====================================================================================================
Helper function for the VideoPyToolbox

MIT License Copyright (c) 2021 GuillermoHidalgoGadea.com

Sourcecode: https://github.com/Guillermo-Hidalgo-Gadea/VideoPyToolbox
====================================================================================================
'''

import os                           # paths and terminal commands
from tkinter import filedialog      # interactive interface to selet files 
from datetime import datetime       # get timestamp for filenames 
 

def compress_h265():
    '''
    Video Compression with H265: This function reads video filenames from a list and compresses with H264 codec. Audio is removed. 
    '''
    # select batch to compress multiple

    videofile = filedialog.askopenfilenames(title='Choose Video Files you want to compress')
    if not videofile:
        return

    # crf from 0 to 51, 18 recommended lossless average
    crf = input("Choose constant rate factor between 0-50: ") or 18

    outputdir = filedialog.askdirectory(title='Choose Output Directory for Compression')
    if not outputdir:
        print('Please select a valid output directory')
        secondtry = filedialog.askdirectory(title='Choose Output Directory for Concatenation')
        if not secondtry:
            return
        else:
            outputdir = secondtry
            
    path = outputdir + '/compressed/'
    
    # set output directory
    try:
        os.mkdir(path)
    except:
        pass

    # compress videos with chosen encoder 
    encoder = input("Choose encoder for compression [x264/x265]: ")

    if '5' in encoder:
        for video in videofile:
            filename = video[:-4]
            output = path + os.path.basename(filename) + '_h265.mp4'
            
            # save metadata
            timestamp = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")
            metadata = path + '/' + 'compression_' + timestamp  + '.txt'

            ffmpeg_command = f"ffmpeg -progress {metadata} -i {video} -an -vcodec libx265 -crf {crf} {output}" 
            os.system(ffmpeg_command)
    else:
        for video in videofile:
            filename = video[:-4]
            output = path + os.path.basename(filename) + '_h264.mp4'

            # save metadata
            timestamp = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")
            metadata = path + '/' + 'compression_' + timestamp  + '.txt'

            ffmpeg_command = f"ffmpeg -progress {metadata} -i {video} -an -vcodec libx264 -crf {crf} {output}" #libx265 not in macos
            os.system(ffmpeg_command)