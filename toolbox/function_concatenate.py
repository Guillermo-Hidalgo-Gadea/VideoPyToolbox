'''
====================================================================================================
Helper function for the VideoPyToolbox

MIT License Copyright (c) 2022 GuillermoHidalgoGadea.com

Sourcecode: https://github.com/Guillermo-Hidalgo-Gadea/VideoPyToolbox
====================================================================================================
'''

import os                           # paths and terminal commands
import numpy as np                  # use arrays in concat
from tkinter import filedialog      # interactive interface to selet files 
from natsort import natsorted, ns   # natural sorting of strings with numbers
from datetime import datetime       # get timestamp for filenames 


def concat_videos():
    '''
    Video concatenation: This function reads video filenames from a list and concatenates conserving the codec. 
    '''
    next = 'y'

    while True:

        if next == 'y':
            # select videos to append
            concatlist= filedialog.askopenfilenames(title='Choose Video Files you want to concatenate')
            if not concatlist:
                return

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
            next = input(f"Concatenate more sessions [y/N]: ")

        if next =='n':
            # ask output directory
            outputdir =filedialog.askdirectory(title='Choose Output Directory for Concatenation')
            if not outputdir:
                print('Please select a valid output directory')
                secondtry = filedialog.askdirectory(title='Choose Output Directory for Concatenation')
                if not secondtry:
                    return

            # find unique output names in concats
            for outputfile in np.unique(concats[:,1]):
    	        # get all filenames that correspond to output
                filenames = concats[concats[:,1]==outputfile][:,0]

                # set output directory
                #output = os.path.join(videopath , "concatenated", outputfile)
                output = os.path.join(outputdir, outputfile)

                # write mylist.txt for ffmpeg
                path, _ = os.path.split(filenames[0])
                myfile = path + "/mylist.txt"
                with open(myfile, "w+") as textfile:
                    for element in filenames:
                        _, name = os.path.split(element)
                        textfile.write("file " +"'"+ name + "'\n")
                    textfile.close()

                # save metadata
                timestamp = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")
                #metadata = os.path.dirname(output) + '/' + 'metadata_' + timestamp  + '.txt'
                progress = os.path.dirname(output) + '/' + 'progress_' + timestamp  + '.txt'

                # concatenate file
                ffmpeg_command = f"ffmpeg -progress {progress} -f concat -safe 0 -i {myfile} -c copy {output}"
                os.system(ffmpeg_command)
                os.remove(myfile)
            
            # if finished print metadata.txt with output duration and size
            metadata = os.path.join(os.path.dirname(output), f"Concat_{timestamp}.txt")
            np.savetxt(metadata, concats, fmt = "%s")

            #break while loop
            break