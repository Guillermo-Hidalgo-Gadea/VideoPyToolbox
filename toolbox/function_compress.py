'''
====================================================================================================
Helper function for the VideoPyToolbox

MIT License Copyright (c) 2022 GuillermoHidalgoGadea.com

Sourcecode: https://github.com/Guillermo-Hidalgo-Gadea/VideoPyToolbox
====================================================================================================
'''

import os                           # paths and terminal commands
from tkinter import filedialog      # interactive interface to selet files  

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
            
    # compress videos with libx265 encoder 
    print("HEVC/H265 compression...")
    # crf from 0 to 51, 12 recommended for lossless average
    crf = input("Choose constant rate factor between 0-50: ") or 12

    # set output filenames
    path = outputdir
    outputs = [path + 'h265_crf{crf}_' + os.path.basename(filename) for filename in videofile]

    for i, video in enumerate(videofile):
        output = outputs[i].split('.')[0] # strip video container

        ffmpeg_command = f"ffmpeg -y -i {video} -an -dn -vcodec libx265 -crf {crf} {output}.mp4" 
        os.system(ffmpeg_command)

def compress_h264():
    '''
    Video Compression with H264: This function reads video filenames from a list and compresses with H264 codec. Audio is removed. 
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
            
    # compress videos with libx265 encoder 
    print("AVC/H264 compression...")
    # crf from 0 to 51, 12 recommended for lossless average
    crf = input("Choose constant rate factor between 0-50: ") or 12

    # set output filenames
    path = outputdir
    outputs = [path + 'h264_crf{crf}_' + os.path.basename(filename) for filename in videofile]

    for i, video in enumerate(videofile):
        output = outputs[i].split('.')[0] # strip video container

        ffmpeg_command = f"ffmpeg -y -i {video} -an -dn -vcodec libx264 -crf {crf} {output}.mp4" 
        os.system(ffmpeg_command)

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
            
    # compress videos with hevc_nvenc encoder 
    print("HEVC_NVENC compression...")
    cq = input("Choose constant quantization parameter between 0-50: ") or 12

    # set output directory
    path = outputdir
    outputs = [path + 'hevc_nvenc_cq{cq}_' + os.path.basename(filename) for filename in videofile]

    for i, video in enumerate(videofile):
        output = outputs[i].split('.')[0] # strip video container

        ffmpeg_command = f"ffmpeg -y -i {video} -an -vcodec hevc_nvenc -preset p7 -rc vbr -cq {cq} {output}.mp4" 
        os.system(ffmpeg_command)
