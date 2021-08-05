"""
====================================================================================================
This VideoPyToolbox uses ffmpeg to play and edit video files from the terminal.
The functions ffplay(), compress_h265(crf), concat_videos() and trim_and_split() are used
to play a video recording, compress it using h265 codec, or to concatenate and trim clips from 
timestamps. Use the custom pipeline to compress and concat at once. 

'conda install ffmpeg' if not already installed

MIT License Copyright (c) 2021 GuillermoHidalgoGadea.com

Sourcecode: https://github.com/Guillermo-Hidalgo-Gadea/VideoPyToolbox
====================================================================================================
"""

# import libraries 
import os                           # paths and terminal commands
import time                         # sleep to slow terminal outputs
import sys, subprocess              # terminal commands in macos
import textwrap                     # clean terminal print

# import functions
from toolbox.function_ffplay import ffplay
from toolbox.function_compress import compress_h265
from toolbox.function_concatenate import concat_videos
from toolbox.function_custom import the_usual
from toolbox.function_rename import batch_rename
from toolbox.function_split import trim_split
from toolbox.logo import ascii_logo, width, height

# Helper functions
def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])
    return

def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')
    return

def reset_terminal(w, h):
    clear()
    cmd = f"mode {w},{h}"
    os.system(cmd)
    
RESET = "\033[0;0m"
MATRIX = "\033[0;32m"

# Entry point
if __name__ == '__main__':
    choice = 'main'
    while True:
    
        if choice.startswith("main"):
            reset_terminal(width, height)

            # header
            print("#"*width + "\n")
            print("MIT License Copyright (c) 2021 GuillermoHidalgoGadea.com\n".center(width))
            print("#"*width)
            
            #logo in ascii here
            sys.stdout.write(MATRIX)
            print(ascii_logo.center(width))
            sys.stdout.write(RESET)
            instructions = "VideoPy is a FFMPEG wrapper to play videos, to compress and change codecs, as well as to append and split raw videos. You can choose between 'p' for play, 'c' for compress, 'a' for append, 's' for split, or 'q' to quit."
            wrapper = textwrap.TextWrapper(width = width)
            print(wrapper.fill(text=instructions))
            choice = input("\n\nHow can I help you? [P/C/A/S/Q]: ")

        elif choice.startswith("c"):
            # start compression
            print("\nStart compression with ffmpeg... \n")
            compress_h265()
            # reset while loop
            choice = 'main'

        elif choice.startswith("p"):
            print("\nStart playing video in ffplay... \n")
            ffplay()
            # reset while loop
            choice = 'main'
            
        elif choice.startswith("a"):
            print("\nStart appending videos with ffmpeg... \n")
            concat_videos()
            # reset while loop
            choice = 'main'
            
        elif choice.startswith("s"):
            print("\nStart trimming videos in ffmpeg... \n")
            trim_split()
            # reset while loop
            choice = 'main'

        elif choice.startswith("u"):
            print("\nAh, the usual. Comming right up... \n")
            the_usual()
            # reset while loop
            choice = 'main'

        elif choice.startswith("r"):
            print("\nStart renaming files... \n")
            batch_rename()
            # reset while loop
            choice = 'main'
            
        elif choice.startswith("q"):
            clear()
            break
            
        else:
            print("\nSorry, couldn't understand the command... \n")
            time.sleep(3)
            # reset while loop
            choice = 'main'
            

