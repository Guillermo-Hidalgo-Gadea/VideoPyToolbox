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

def trim_split():
    '''
    Video trim: This function reads video filenames and timestamps from a list and trims clips. 
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
    #if check.startswith("n"):
    #    open_file(filename)
    #else:
    # loop over cases and get split command
    for case in range(len(splitlist)):
        row = splitlist[case:case+1]
        row = row.to_string(header=False, index=False).split()
        original = path + '/' + row[0]
        forced = path + '/forces_' + row[0]
        output = os.path.dirname(filename) + '/' + row[1]
        start = row[2]
        end = row[3]

        # save metadata
        timestamp = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")
        metadata = os.path.dirname(filename) + '/' + 'split_' + timestamp  + '.txt'

        # first inster key_frames at timepoint for accurate seeking
        #ffmpeg_command = f"ffmpeg -i {original} -force_key_frames {start},{end} -c copy {forced}"
        #os.system(ffmpeg_command)

        # then overwrite the output trimmed at given timestamps
        #ffmpeg_command = f"ffmpeg -y -i {original} -ss {start} -to {end} -c copy {output} > {metadata} 2>&1" #If you want to save both to go to file > result.txt 2>&1  
        ffmpeg_command = f"ffmpeg -y -progress {metadata} -i {original} -ss {start} -to {end} -c:v ffv1 {output}"
        os.system(ffmpeg_command)

        """
        ATTENTION, -to and -t confounded? splits of different sices...
        -ss works differently before and after -i, after is more frame-accurate 
        Maybe error with Keyframes at given timestamp? 
        Since the seeking operation jumps between I-frames, it is not going to accurately stop on the frame (or time) that you requested. It will search for the nearest I-frame and start the copy operation from that point.
        trim: ffmpeg -i INPUT -vf trim=60:120
        -y to Overwrite output files without asking

        1) use -ss after input to be more accurate
        2) add keyframes at given timestamp...
        3) use recode instead of copy to re-create frames around cut edges, lossless codec ffv1?

        """

        
