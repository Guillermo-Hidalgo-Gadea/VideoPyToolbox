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

# 'conda install ffmpeg' if not already installed

# import libraries 
import os
from tkinter import filedialog


def ffplay():
    '''
    Video player with ffplay instead of OpenCV
    '''
    # Choose Video File from Dialog Box
    videofile = filedialog.askopenfilenames(title='Choose the Video Files you want to play')
    video = videofile[0]

    ffmpeg_command = f"ffplay {video}"
    print(ffmpeg_command)
    os.system(ffmpeg_command)


def play_video():
    '''
    Video player with openCV: DEPRECATED
    '''
    import cv2
    # Choose Video File from Dialog Box
    videofile = filedialog.askopenfilenames(title='Choose the Video Files you want to play')

    # Create a VideoCapture object and read from input file 
    cap = cv2.VideoCapture(videofile[0]) 

    # Calculate Video Properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total/fps

    print("Video Frame Rate: %d FPS" %fps)
    print("Frames contained: %d" %total)
    print("Video duration: %d sec" %duration)


    # Check if camera opened successfully 
    if (cap.isOpened()== False): 
        print("Error opening video file") 

    # Read until video is completed 
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
            
        if ret == True:
            # resize frame
            h, w, c = frame.shape
            frame = cv2.resize(frame, (int(w/1.5), int(h/1.5))) 
            
            # Display the resulting frame
            cv2.imshow('Frame', frame)
        
               
            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release 
    cap.release() 


    # Closes all the frames 
    cv2.destroyAllWindows() 


def compress_h265(crf):
    '''
    Video Compression with H265: This function reads video filenames from a list and compresses with H264 codec. Audio is removed. 
    '''
    videofile = filedialog.askopenfilenames(title='Choose Video Files you want to compress')
    for video in videofile:
        filename = video[:-4]
        output = filename + '_h265.mp4'
        
        # crf from 0 to 51, 18 recommended lossless average
        ffmpeg_command = f"ffmpeg -i {video} -an -vcodec libx265 -crf {crf} {output}"
        print(ffmpeg_command)
        os.system(ffmpeg_command)
	# color settings: ffmpeg -i input -vf format=gray output

         
def concat_videos():
    '''
    Video concatenation: This function reads video filenames from a list and concatenates conserving the codec. 
    '''
    # select videos to append and write to txt
    concatlist= filedialog.askopenfilenames(title='Choose Video Files you want to concatenate')
    ## ??? video ORDER?
    with open("mylist.txt", "w+") as textfile:
        for element in concatlist:
            textfile.write("file " +"'"+ element + "'\n")
        textfile.close()

    # name output file
    output = input(f"Output filename for {concatlist[0]}: ")
    output = output + '.mp4'
    
    ffmpeg_command = f"ffmpeg -f concat -safe 0 -i mylist.txt -c copy {output}"
    print(ffmpeg_command)
    os.system(ffmpeg_command)


def trim_and_split():
    '''
    Video trim: This function reads video filenames and timestamps from a list and trims clips. 
    '''
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
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("########################################################")
        print("           Welcome to the the VideoPyToolbox            ")
        print("MIT License Copyright (c) 2021 GuillermoHidalgoGadea.com")
        print("########################################################")
        print("\n\nYou can Play, Compress, Append and Trim videos, right from the terminal")
        print("[choose between 'p','c','a','t' and 'q' to play, compress, append, trim and quit]")

        choice = input("\n\nHow can I help you? (P/C/A/T/Q): ")

    
