'''
====================================================================================================
Helper function for the VideoPyToolbox

MIT License Copyright (c) 2021 GuillermoHidalgoGadea.com

Sourcecode: https://github.com/Guillermo-Hidalgo-Gadea/VideoPyToolbox
====================================================================================================
'''

import os                           # paths and terminal commands
import pandas as pd                 # data frames for metadata
from tkinter import filedialog      # interactive interface to selet files 
from datetime import datetime       # get timestamp for filenames 

def compress_h265():
    '''
    Video Compression with H265: This function reads video filenames from a list and compresses with H265 codec. Audio is removed. 
    '''
    # select batch to compress multiple
    videofile = list(filedialog.askopenfilenames(title='Choose Video Files you want to compress'))
    if not videofile:
        return

    outputdir = filedialog.askdirectory(title='Choose Output Directory for Compression')
    if not outputdir:
        print('Please select a valid output directory')
        secondtry = filedialog.askdirectory(title='Choose Output Directory for Concatenation')
        if not secondtry:
            return
        else:
            outputdir = secondtry
            
    # set output directory
    path = outputdir + '/compressed/'
    try:
        os.mkdir(path)
    except:
        pass

    outputs = [path + 'h265_' + os.path.basename(filename) for filename in videofile]

    # compress videos with libx265 encoder 
    
    # crf from 0 to 51, 18 recommended lossless average
    print("HEVC/H265 compression...")
    crf = input("Choose constant rate factor between 0-50: ") or 18

    starttime = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")

    for i, video in enumerate(videofile):
        output = outputs[i]

        ffmpeg_command = f"ffmpeg -y -i {video} -an -vcodec libx265 -crf {crf} {output}" 
        os.system(ffmpeg_command)

    endtime = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")

    # save metadata
    metadata = path + '/' + 'h265_compression_' + starttime  + '.txt'
    filelist = pd.DataFrame({'input': videofile, 'output': outputs}, index=None)
    filelist.to_csv(metadata, sep ='\t', index=False)
    # add header
    title = f"# VideoPyToolbox compression with libx265 crf={crf} \n # started: {starttime} ended: {endtime} \n"
    with open(metadata, "r+") as textfile:
        original = textfile.read()
        textfile.seek(0)
        textfile.write(title + original)
        textfile.close()


def compress_hevc_nvenc():
    '''
    Video Compression with HEVC_NVENC: This function reads video filenames from a list and compresses with hardware accelerated encoding. Audio is removed. 
    '''
    # select batch to compress multiple
    videofile = list(filedialog.askopenfilenames(title='Choose Video Files you want to compress'))
    if not videofile:
        return

    outputdir = filedialog.askdirectory(title='Choose Output Directory for Compression')
    if not outputdir:
        print('Please select a valid output directory')
        secondtry = filedialog.askdirectory(title='Choose Output Directory for Concatenation')
        if not secondtry:
            return
        else:
            outputdir = secondtry
            
    # set output directory
    path = outputdir + '/compressed/'
    try:
        os.mkdir(path)
    except:
        pass

    outputs = [path + 'hevc_nvenc_' + os.path.basename(filename) for filename in videofile]

    # compress videos with hevc_nvenc encoder 
    print("HEVC_NVENC compression...")
    cq = input("Choose constant quantization parameter between 0-50: ") or 18

    starttime = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")

    for i, video in enumerate(videofile):
        output = outputs[i]

        ffmpeg_command = f"ffmpeg -y -i {video} -an -vcodec hevc_nvenc -preset p7 -rc vbr -cq {cq} {output}" 
        os.system(ffmpeg_command)

    endtime = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")

    # save metadata
    metadata = path + '/' + 'hevc_nvenc_compression_' + starttime  + '.txt'
    filelist = pd.DataFrame({'input': videofile, 'output': outputs}, index=None)
    filelist.to_csv(metadata, sep ='\t', index=False)
    # add header
    title = f"# VideoPyToolbox compression with hevc_nvenc preset=p7, rc=vbr, cq={cq} \n # started: {starttime} ended: {endtime}"
    with open(metadata, "r+") as textfile:
        original = textfile.read()
        textfile.seek(0)
        textfile.write(title + original)
        textfile.close()