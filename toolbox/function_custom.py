'''
====================================================================================================
Helper function for the VideoPyToolbox

MIT License Copyright (c) 2021 GuillermoHidalgoGadea.com

Sourcecode: https://github.com/Guillermo-Hidalgo-Gadea/VideoPyToolbox
====================================================================================================
'''

import os                           # paths and terminal commands
import numpy as np                  # use arrays in concat
from tkinter import filedialog      # interactive interface to selet files 
from natsort import natsorted, ns   # natural sorting of strings with numbers
from datetime import datetime       # get timestamp for filenames 


def the_usual_h265():
    '''
    The usual is a custom pipeline to concat and compress video snippets at once. See concat_videos and compress_h265 for doing the processing in separate steps.
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
            output = [output + '_h265.mp4'] * len(filenames)

            # append or create concatenation dataset
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

            # set compression
            print("HEVC/H265 compression...")
            crf = input("Choose constant rate factor between 0-50: ") or 18

            starttime = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")

            # find unique output names in concats
            for outputfile in np.unique(concats[:,1]):
    	        # get all filenames that correspond to output
                filenames = concats[concats[:,1]==outputfile][:,0]

                # set output directory
                output = os.path.join(outputdir , "concatenated", outputfile)

                try:
                    os.mkdir(os.path.dirname(output))
                except:
                    pass

                # write mylist.txt for ffmpeg
                path, _ = os.path.split(filenames[0])
                myfile = path + "/mylist.txt"
                with open(myfile, "w+") as textfile:
                    for element in filenames:
                        _, name = os.path.split(element)
                        textfile.write("file " +"'"+ name + "'\n")
                    textfile.close()

                # concatenate file with re-encoding
                ffmpeg_command = f"ffmpeg -y -f concat -safe 0 -i {myfile} -an -vcodec libx265 -crf {crf} {output}"
                os.system(ffmpeg_command)
                os.remove(myfile)
            
            endtime = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")

            # save metadata
            metadata = outputdir + '/' + 'concat_compression_' + starttime  + '.txt'
            np.savetxt(metadata, concats, fmt = "%s")

            # add header
            title = f"# VideoPyToolbox concat_compression with libx265 crf={crf}, started: {starttime} ended: {endtime}"
            with open(metadata, "r+") as textfile:
                original = textfile.read()
                textfile.seek(0)
                textfile.write(title + original)
                textfile.close()

            #break while loop
            break

def the_usual_hevc_nvenc():
    '''
    The usual is a custom pipeline to concat and compress video snippets at once. See concat_videos and compress_hevc_nvenc for doing the processing in separate steps.
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
            output = [output + '_h265.mp4'] * len(filenames)

            # append or create concatenation dataset
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

            # set compression
            print("HEVC_NVENC compression...")
            cq = input("Choose constant quantization parameter between 0-50: ") or 18

            starttime = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")

            # find unique output names in concats
            for outputfile in np.unique(concats[:,1]):
    	        # get all filenames that correspond to output
                filenames = concats[concats[:,1]==outputfile][:,0]

                # set output directory
                output = os.path.join(outputdir , "concatenated", outputfile)

                try:
                    os.mkdir(os.path.dirname(output))
                except:
                    pass

                # write mylist.txt for ffmpeg
                path, _ = os.path.split(filenames[0])
                myfile = path + "/mylist.txt"
                with open(myfile, "w+") as textfile:
                    for element in filenames:
                        _, name = os.path.split(element)
                        textfile.write("file " +"'"+ name + "'\n")
                    textfile.close()

                # concatenate file with re-encoding
                ffmpeg_command = f"ffmpeg -y -f concat -safe 0 -i {myfile} -an -vcodec hevc_nvenc -preset p7 -rc vbr -cq {cq} {output}"
                os.system(ffmpeg_command)
                os.remove(myfile)
            
            endtime = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")

            # save metadata
            metadata = outputdir + '/' + 'concat_compression_' + starttime  + '.txt'
            np.savetxt(metadata, concats, fmt = "%s")

            # add header
            title = f"# VideoPyToolbox concat_compression with hevc_nvenc preset=p7, rc=vbr, cq={cq}, started: {starttime} ended: {endtime}"
            with open(metadata, "r+") as textfile:
                original = textfile.read()
                textfile.seek(0)
                textfile.write(title + original)
                textfile.close()

            #break while loop
            break