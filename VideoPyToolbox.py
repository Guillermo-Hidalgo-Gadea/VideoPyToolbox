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
- trim and split function


Pipeline:
1) compress all videos to a common codec (h.265/h.264) to save space
2) concatenate videos to complete sessions
3) manually set timestamps for start/end as well as trial length
4) loop over csv file and trim/split all files
5) new folder with individual trials
'''


# 'conda install ffmpeg' if not already installed

# import libraries 
import os
import numpy as np
from tkinter import filedialog      # interactive interface to selet files 
from natsort import natsorted, ns   # natural sorting of strings with numbers
from datetime import datetime       # get timestamp for filenames 


def ffplay():
    '''
    Video player with ffplay instead of OpenCV
    '''
    # Choose Video File from Dialog Box
    videofile = filedialog.askopenfilenames(title='Choose the Video Files you want to play')
    video = videofile[0]

    ffmpeg_command = f"ffplay {video}"
    #print(ffmpeg_command)
    os.system(ffmpeg_command)


def compress_h265(crf):
    '''
    Video Compression with H265: This function reads video filenames from a list and compresses with H264 codec. Audio is removed. 
    '''
    videofile = filedialog.askopenfilenames(title='Choose Video Files you want to compress')
    for video in videofile:
        filename = video[:-4]
        output = filename + '_h265.mp4'
        
        # crf from 0 to 51, 18 recommended lossless average
        ffmpeg_command = f"ffmpeg -i {video} -an -vcodec libx265 -crf {crf} {output}" #libx265 not in macos
        #print(ffmpeg_command)
        os.system(ffmpeg_command)
	# color settings: ffmpeg -i input -vf format=gray output

         
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
            _, name1 = os.path.split(filenames[0])
            _, name2 = os.path.split(filenames[-1])
            output = input(f"Output filename for {name1} to {name2}: ")
            output = [output + '.mp4'] * len(filenames)
            
            # append or create concatination dataset
            try:
                concats = np.vstack((concats, np.column_stack((filenames, output))))
            except:
                concats = np.column_stack((filenames, output))
            
            # repeat for other sessions...
            next = input(f"Concatenate more sessions [y/n]: ")

        if next =='n':
            # start the actual concatenation
            
            timestamp = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")

            # find unique output names in concats
            for outputfile in np.unique(concats[:,1]):
    	        # get all filenames that correspond to output
                filenames = concats[concats[:,1]==outputfile][:,0]

                # set output directory
                output = os.path.join(os.path.dirname(filenames[0]) , "concatenated", outputfile)
                path, _ = os.path.split(output)
                try:
                    os.mkdir(path)
                except:
                    pass

                # set ffmpeg parameters
                mylist = os.path.join(path, "mylist.txt")
                with open(mylist, "w+") as textfile:
                    for element in filenames:
                        textfile.write("file " +"'"+ element + "'\n")
                    textfile.close()

                # concatenate file
                ffmpeg_command = f"ffmpeg -f concat -safe 0 -i {mylist} -c copy {output}"
                    #print(ffmpeg_command)
                os.system(ffmpeg_command)
                os.remove(mylist)
            
            # if finished print metadata.txt with output duration and size
            metadata = os.path.join(path, f"Concatenation_{timestamp}_VideoPyToolbox.txt")
            np.savetxt(metadata, concats, fmt = "%s")

            #break while loop
            break


def trim_and_split():
    '''
    Video trim: This function reads video filenames and timestamps from a list and trims clips. 
    '''
    # select all files to trim and split
    # create template csv
    # open and edit csv timestamps
    # check csv format
    # loop over cases and split 
    pass
    

## Entry point
choice = ''

while True:
    
    if choice.startswith("c"):
        # start compression
        print("\nStart video compression in ffmpeg with H265 codec... \n")
        crf = input("Choose constant rate factor between 0-50: ")
        compress_h265(crf)
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
        
    elif choice.startswith("t"):
        print("\nStart trimming videos in ffmpeg... \n")
        # reset while loop
        choice = ''
        
    elif choice.startswith("q"):
        break
        
    else:
        print("########################################################")
        print("           Welcome to the the VideoPyToolbox            ")
        print("MIT License Copyright (c) 2021 GuillermoHidalgoGadea.com")
        print("########################################################")
        print("\n\nYou can Play, Compress, Append and Trim videos, right from the terminal")
        print("[choose between 'p','c','a','t' and 'q' to play, compress, append, trim and quit]")

        choice = input("\n\nHow can I help you? (P/C/A/T/Q): ")

    
