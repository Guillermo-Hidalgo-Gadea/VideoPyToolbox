"""
====================================================================================================
This VideoPyToolbox uses ffmpeg to play and edit video files from the terminal.
The functions ffplay(), compress_h265(crf), concat_videos() and trim_and_split() are used
to play a video recording, compress it using h265 codec, or to concatenate and trim clips from 
timestamps.

MIT License Copyright (c) 2021 GuillermoHidalgoGadea.com

Sourcecode: https://github.com/Guillermo-Hidalgo-Gadea/VideoPyToolbox
====================================================================================================
"""

'''
## TODO: 
- separate functions in modules
- get timestamps to trim from player


Pipeline:
1) compress all videos to a common codec (h.265/h.264) to save space
2) concatenate videos to complete sessions
3) manually set timestamps for start/end as well as trial length
4) loop over csv file and trim/split all files
5) new split folder with individual trials
'''


# 'conda install ffmpeg' if not already installed

# import libraries 
import os                           # paths and terminal commands
import sys, subprocess              # terminal commands in macos
import textwrap                     # clean terminal print
import numpy as np                  # use arrays in concat
import pandas as pd                 # data frames in split
from tkinter import filedialog      # interactive interface to selet files 
from natsort import natsorted, ns   # natural sorting of strings with numbers
from datetime import datetime       # get timestamp for filenames 
#import ffpb                        # wrap ffmpeg in ffpb to show progress bar
#pip install ffpb                   

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

def clear():
      
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

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


def compress_h265():
    '''
    Video Compression with H265: This function reads video filenames from a list and compresses with H264 codec. Audio is removed. 
    '''
    videofile = filedialog.askopenfilenames(title='Choose Video Files you want to compress')
    
    # crf from 0 to 51, 18 recommended lossless average
    crf = input("Choose constant rate factor between 0-50: ") or 18

    path = os.path.dirname(videofile[0]) + '/compressed/'
    
    # set output directory
    try:
        os.mkdir(path)
    except:
        pass

    # compress videos with chosen encoder 
    encoder = input("Choose encoder for compression [x264/x265]: ")

    # save metadata
    timestamp = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")
    metadata = path + '/' + 'compression_' + timestamp  + '.txt'

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

         
def concat_videos():
    '''
    Video concatenation: This function reads video filenames from a list and concatenates conserving the codec. 
    '''
    next = 'y'

    while True:

        if next == 'y':
            # select videos to append
            concatlist= filedialog.askopenfilenames(title='Choose Video Files you want to concatenate')

            # maintain natural order of strings with numbers
            filenames = list(natsorted(concatlist, alg=ns.IGNORECASE))

            # give common output filename
            videopath, name1 = os.path.split(filenames[0])
            _, name2 = os.path.split(filenames[-1])
            output = input(f"Output filename for {name1} to {name2}: ")
            output = [output + '.mp4'] * len(filenames)

            # append or create concatination dataset
            try:
                concats = np.vstack((concats, np.column_stack((filenames, output))))
            except:
                concats = np.column_stack((filenames, output))
            
            # repeat for other sessions...
            next = input(f"Concatenate more sessions [y/N]: ")

        if next =='n':
            # start the actual concatenation
            timestamp = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")

            # find unique output names in concats
            for outputfile in np.unique(concats[:,1]):
    	        # get all filenames that correspond to output
                filenames = concats[concats[:,1]==outputfile][:,0]

                # set output directory
                output = os.path.join(videopath , "concatenated", outputfile)

                try:
                    os.mkdir(os.path.dirname(output))
                except:
                    pass

                # set ffmpeg parameters
                myfile = videopath + "/mylist.txt"
                with open(myfile, "w+") as textfile:
                    for element in filenames:
                        _, name = os.path.split(element)
                        textfile.write("file " +"'"+ name + "'\n")
                    textfile.close()

                # save metadata
                timestamp = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")
                metadata = os.path.dirname(output) + '/' + 'concat_' + timestamp  + '.txt'

                # concatenate file
                ffmpeg_command = f"ffmpeg -progress {metadata} -f concat -safe 0 -i {myfile} -c copy {output}"
                os.system(ffmpeg_command)
                os.remove(myfile)
            
            # if finished print metadata.txt with output duration and size
            metadata = os.path.join(os.path.dirname(output), f"Concat_{timestamp}.txt")
            np.savetxt(metadata, concats, fmt = "%s")

            #break while loop
            break


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
    instruction = '# This is a list of videos to split with VideoPyToolbox.\n# Please edit the parameters below and save the file.\n#To split one input into several outputs copy/paste the respective line.\n'
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
        output = os.path.dirname(filename) + '/' + row[1]
        start = row[2]
        end = row[3]

        # save metadata
        timestamp = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")
        metadata = os.path.dirname(filename) + '/' + 'split_' + timestamp  + '.txt'

        #ffmpeg_command = f"ffmpeg -ss {start} -i {original} -to {end} -c copy {output} > {metadata} 2>&1" #If you want both to go to file > result.txt 2>&1
        #ffmpeg_command = f"ffpb -ss {start} -i {original} -to {end} -c copy {output} 2> {metadata}"  #if you use 2> than STDERR goes to file
        #ffmpeg_command = f"ffpb -ss {start} -i {original} -to {end} -c copy {output} > {metadata}" # If you use > than STDOUT goes to file.  
        ffmpeg_command = f"ffmpeg -progress {metadata} -ss {start} -i {original} -to {end} -c copy {output}"

        # split in loop
        os.system(ffmpeg_command)


## Entry point
choice = ''

while True:
    
    if choice.startswith("c"):
        # start compression
        print("\nStart video compression in ffmpeg with H265 codec... \n")
        compress_h265()
        # reset while loop
        choice = ''

    elif choice.startswith("p"):
        print("\nStart playing video in ffplay... \n")
        ffplay()
        # reset while loop
        choice = ''
        
    elif choice.startswith("a"):
        print("\nStart appending videos in ffmpeg... \n")
        concat_videos()
        # reset while loop
        choice = ''
        
    elif choice.startswith("s"):
        print("\nStart trimming videos in ffmpeg... \n")
        trim_split()
        # reset while loop
        choice = ''
        
    elif choice.startswith("q"):
        clear()
        break
        
    else:
        clear()
        terminalwidth = os.get_terminal_size().columns
        print("#"*terminalwidth)
        print("Welcome to the VideoPy Toolbox".center(terminalwidth))
        print("MIT License Copyright (c) 2021 GuillermoHidalgoGadea.com".center(terminalwidth))
        print("#"*terminalwidth)
        print("\n\n")
        instructions = "VideoPy is a FFMPEG wrapper to play videos, to compress and change codecs, as well as to append and split raw videos. You can choose between 'p' for play, 'c' for compress, 'a' for append, 's' for split, or 'q' to quit."
        wrapper = textwrap.TextWrapper(width = terminalwidth)
        print(wrapper.fill(text=instructions))
        choice = input("\n\nHow can I help you? [P/C/A/S/Q]: ")

    
