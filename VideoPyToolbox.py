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
import sys                          # terminal commands in macos
import textwrap                     # clean terminal print
import GPUtil                       # check available GPUs

# import functions
from toolbox.function_ffplay import ffplay
from toolbox.function_compress import compress_h265, compress_hevc_nvenc
from toolbox.function_concatenate import concat_videos
from toolbox.function_custom import the_usual_h265, the_usual_hevc_nvenc
from toolbox.function_rename import batch_rename
from toolbox.function_split import trim_split_h265, trim_split_hevc_nvenc
from toolbox.logo import ascii_logo, width, height

# Helper functions
def reset_terminal(w, h):
    if os.name == 'nt': # for windows
        _ = os.system('cls')
        cmd = f"mode {w},{h}"
        os.system(cmd)  
    else:# for mac and linux(here, os.name is 'posix')
        _ = os.system('clear')
        cmd = f"mode {w},{h}"
        os.system(cmd)    

def check_gpu():
    gpu_detect = GPUtil.getAvailable()
    if gpu_detect:
        print("GPU detected!")
        GPUtil.showUtilization(all=True)
        gpu_use = input("Would you like to use GPU accelerated encoding? [y/N]")
    else:
        gpu_use = 'n'
    return gpu_use

# Terminal print colors
RESET = "\033[0;0m"
MATRIX = "\033[0;32m"
CYAN = "\033[0;36m"
RED = "\033[0;31m"


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
            instructions = "VideoPy is a FFMPEG wrapper to play videos, to compress and change codecs, as well as to append and split raw videos."
            wrapper = textwrap.TextWrapper(width = width)
            print(wrapper.fill(text=instructions))
            # function help format
            help = '''
        'p'     Play audio or video file
        'c'     Compress video to h.265/h.264
        'a'     Append or Concatenate multiple files
        's'     Split or Trim files by timestamp 
        'r'     Rename files in batches
        'u'     Custom pipeline to compress and concatenate
        'gpu'   Check GPU for hardware acceleration
        'q'     Quit
            '''

            print(help)

            choice = input("\n(CPU mode) How can I help you: ")
        
        elif "acc_main" in choice:
            reset_terminal(width, height)

            # header
            print("#"*width + "\n")
            print("MIT License Copyright (c) 2021 GuillermoHidalgoGadea.com\n".center(width))
            print("#"*width)
            
            #logo in ascii here
            sys.stdout.write(CYAN)
            print(ascii_logo.center(width))
            sys.stdout.write(RESET)
            instructions = "VideoPy is a FFMPEG wrapper to play videos, to compress and change codecs, as well as to append and split raw videos."
            wrapper = textwrap.TextWrapper(width = width)
            print(wrapper.fill(text=instructions))
            # function help format
            help = '''
        'p'     Play audio or video file
        'c'     Compress video to h.265/h.264
        'a'     Append or Concatenate multiple files
        's'     Split or Trim files by timestamp 
        'r'     Rename files in batches
        'u'     Custom pipeline to compress and concatenate
        'gpu'   Check GPU for hardware acceleration
        'q'     Quit
            '''
            print(help)

            choice = input("\n(GPU mode) How can I help you: ")

        elif "g" in choice:
            gpu_use = check_gpu()
            if "y" not in gpu_use:
                choice = 'main'
            else:
                choice = 'acc_main'

        elif choice.startswith("p"):
            print("\nStart playing video in ffplay... \n")
            ffplay()
            input("\nVideo ended!\n")
            # reset while loop
            choice = 'main'
            
        elif choice.startswith("c"):
            # start compression
            print("\nStart compression with ffmpeg... \n")
            if "y" not in gpu_use:
                compress_h265()
                input("\nCompressing ended!\n")
                # reset while loop
                choice = 'main'
            else:
                compress_hevc_nvenc()
                input("\nCompressing ended!\n")
                # reset while loop
                choice = 'acc_main'
            
        elif choice.startswith("a"):
            print("\nStart appending videos with ffmpeg... \n")
            concat_videos()
            input("\nAppending ended!\n")
            # reset while loop
            choice = 'main'
            
        elif choice.startswith("s"):
            print("\nStart trimming videos in ffmpeg... \n")
            if "y" not in gpu_use:
                trim_split_h265()
                input("\nTrimming ended!\n")
                # reset while loop
                choice = 'main'
            else:
                trim_split_hevc_nvenc()
                input("\nTrimming ended!\n")
                # reset while loop
                choice = 'acc_main'

        elif choice.startswith("u"):
            print("\nAh, the usual. Comming right up... \n")
            if "y" not in gpu_use:
                the_usual_h265()
                input("\nPipeline ended!\n")
                # reset while loop
                choice = 'main'
            else:
                the_usual_hevc_nvenc()
                input("\nPipeline ended!\n")
                # reset while loop
                choice = 'acc_main'

        elif choice.startswith("r"):
            print("\nStart renaming files... \n")
            batch_rename()
            input("\nRenaming ended!\n")
            # reset while loop
            choice = 'main'
            
        elif choice.startswith("q"):
            break
            
        else:
            print("\nSorry, couldn't understand the command... \n")
            time.sleep(1.5)
            # reset while loop
            if "y" in gpu_use:
                choice = 'acc_main'
            else:
                choice = 'main'
            

