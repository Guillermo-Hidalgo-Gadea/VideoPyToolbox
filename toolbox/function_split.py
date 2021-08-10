'''
====================================================================================================
Helper function for the VideoPyToolbox

MIT License Copyright (c) 2021 GuillermoHidalgoGadea.com

Sourcecode: https://github.com/Guillermo-Hidalgo-Gadea/VideoPyToolbox
====================================================================================================
'''

import os                           # paths and terminal commands
import pandas as pd                 # data frames in split
import sys, subprocess              # terminal commands in macos
from tkinter import filedialog      # interactive interface to selet files 
from datetime import datetime       # get timestamp for filenames 

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])
    return

def trim_split_h265():
    '''
    Video trim: This function reads video filenames and timestamps from a list and trims clips by re-encoding lossless with libx265 crf=0. 
    '''
    # select videos to split
    splitlist= filedialog.askopenfilenames(title='Choose Video Files you want to split')
    path = os.path.dirname(splitlist[0])
    splitlist = [os.path.basename(filename) for filename in splitlist]

    # placeholders
    output = ['trim_' + filename for filename in splitlist]
    start = ['00:00:00.000'] * len(splitlist)
    end = ['00:00:00.000'] * len(splitlist)
    
    timestamp = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")
    filename = path + '/split/' + timestamp + '_' + 'splitlist.txt' 
    # set output directory
    try:
        os.mkdir(os.path.dirname(filename))
    except:
        pass

    # create template csv
    splitlist = pd.DataFrame({'input': splitlist, 'output': output, 'start':start, 'end':end}, index=None)
    
    splitlist.to_csv(filename, sep ='\t', index=False)

    # add instructions
    instruction = '# Splitting files  with VideoPyToolbox.\n# Please edit the parameters below and save the file.\n#To split one input into several outputs copy/paste the respective line.\n'
    with open(filename, "r+") as textfile:
        original = textfile.read()
        textfile.seek(0)
        textfile.write(instruction + original)
        textfile.close()
    
    # open and edit csv timestamps
    open_file(filename)

    input("Continue splitting?")

    # check csv format
    splitlist = pd.read_csv(filename, sep ='\t', comment='#')
    print(filename)
    print(splitlist)
    check = input('Is the format correct? [y/n] ')
    if "n" in check:
        open_file(filename)
        second_check = input('Is the format correct? [y/n] ')
        if "n" in second_check:
            return
    else:
        starttime = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")
        # loop over cases in file
        for case in range(len(splitlist)):
            row = splitlist[case:case+1]
            row = row.to_string(header=False, index=False).split()
            original = path + '/' + row[0]
            output = os.path.dirname(filename) + '/' + row[1]
            start = row[2]
            end = row[3]

            # split with re-encoding
            ffmpeg_command = f"ffmpeg -y -i {original} -ss {start} -to {end} -vcodec libx265 -crf 0 {output}"
            os.system(ffmpeg_command)
        
        endtime = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")
        # add instructions
        header = f"# started: {starttime} ended: {endtime}, re-encoded libx265 crf=0\n"
        with open(filename, "r+") as textfile:
            original = textfile.read()
            textfile.seek(0)
            textfile.write(header + original)
            textfile.close()


def trim_split_hevc_nvenc():
    '''
    Video trim: This function reads video filenames and timestamps from a list and trims clips by re-encoding lossless with hevc_nvenc cq=0. 
    '''
    # select videos to split
    splitlist= filedialog.askopenfilenames(title='Choose Video Files you want to split')
    path = os.path.dirname(splitlist[0])
    splitlist = [os.path.basename(filename) for filename in splitlist]

    # placeholders
    output = ['trim_' + filename for filename in splitlist]
    start = ['00:00:00.000'] * len(splitlist)
    end = ['00:00:00.000'] * len(splitlist)
    
    timestamp = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")
    filename = path + '/split/' + timestamp + '_' + 'splitlist.txt' 
    # set output directory
    try:
        os.mkdir(os.path.dirname(filename))
    except:
        pass

    # create template csv
    splitlist = pd.DataFrame({'input': splitlist, 'output': output, 'start':start, 'end':end}, index=None)
    
    splitlist.to_csv(filename, sep ='\t', index=False)

    # add instructions
    instruction = '# Splitting files  with VideoPyToolbox.\n# Please edit the parameters below and save the file.\n#To split one input into several outputs copy/paste the respective line.\n'
    with open(filename, "r+") as textfile:
        original = textfile.read()
        textfile.seek(0)
        textfile.write(instruction + original)
        textfile.close()
    
    # open and edit csv timestamps
    open_file(filename)

    input("Continue splitting?")

    # check csv format
    splitlist = pd.read_csv(filename, sep ='\t', comment='#')
    print(filename)
    print(splitlist)
    check = input('Is the format correct? [y/n] ')
    if "n" in check:
        open_file(filename)
        second_check = input('Is the format correct? [y/n] ')
        if "n" in second_check:
            return
    else:
        starttime = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")
        # loop over cases in file
        for case in range(len(splitlist)):
            row = splitlist[case:case+1]
            row = row.to_string(header=False, index=False).split()
            original = path + '/' + row[0]
            output = os.path.dirname(filename) + '/' + row[1]
            start = row[2]
            end = row[3]

            # split with re-encoding
            ffmpeg_command = f"ffmpeg -y -i {original} -ss {start} -to {end} -vcodec hevc_nvenc -preset p7 -rc vbr -cq 0 {output}"
            os.system(ffmpeg_command)
        
        endtime = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")
        # add instructions
        header = f"# started: {starttime} ended: {endtime}, re-encoded hevc_nvenc preset=p7 rc=vbr cq=0\n"
        with open(filename, "r+") as textfile:
            original = textfile.read()
            textfile.seek(0)
            textfile.write(header + original)
            textfile.close()