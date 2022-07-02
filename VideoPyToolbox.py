"""
====================================================================================================
This VideoPyToolbox uses ffmpeg to play and edit video files from the terminal.
The functions ffplay(), compress_h265(crf), concat_videos() and trim_and_split() are used
to play a video recording, compress it using h265 codec, or to concatenate and trim clips from 
timestamps. Use the custom pipeline to compress and concat at once. 

MIT License Copyright (c) 2022 GuillermoHidalgoGadea.com
 
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
from toolbox.function_compress import compress_h265, compress_h264, compress_hevc_nvenc
from toolbox.function_concatenate import concat_videos
from toolbox.function_custom import the_usual_h265
from toolbox.function_split import trim_split_h265, trim_split_hevc_nvenc
from toolbox.function_mosaic import mosaic_video
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
        show = [[{'attr':'id','name':'ID'},{'attr':'name','name':'Name'}],
                [{'attr':'temperature','name':'GPU temp.','suffix':'C','transform': lambda x: x,'precision':0},
                {'attr':'load','name':'GPU util.','suffix':'%','transform': lambda x: x*100,'precision':0},
                {'attr':'memoryUtil','name':'Memory util.','suffix':'%','transform': lambda x: x*100,'precision':0}]]
        print("\n")
        GPUtil.showUtilization(all=False, attrList=show, useOldCode=False)

        gpu_use = input("\nGPU detected! Use GPU accelerated encoding? [y/N]")
    else:
        gpu_use = 'n'
    return gpu_use

# Terminal print colors
RESET = "\033[0;0m"
MATRIX = "\033[0;32m"
YELLOW = "\033[0;33m"
CYAN = "\033[0;36m"
RED = "\033[0;31m"


# Entry point
if __name__ == '__main__':
    choice = 'main'
    gpu_use = 'n'
    while True:
    
        if choice.startswith("main"):
            reset_terminal(width, height)

            # header
            print("#"*width + "\n")
            print("MIT License Copyright (c) 2022 GuillermoHidalgoGadea.com\n".center(width))
            print("#"*width)
            
            #logo in ascii here
            sys.stdout.write(YELLOW)
            print(ascii_logo.center(width))
            sys.stdout.write(RESET)
            instructions = "VideoPy is a FFMPEG wrapper to play videos, to compress and change codecs, as well as to append and split raw videos."
            wrapper = textwrap.TextWrapper(width = width)
            print(wrapper.fill(text=instructions))
            # function help format
            help = '''
        'p'     Play audio or video file
        'c'     Compress video with h265/h264
        'a'     Append or Concatenate multiple files
        's'     Split or Trim files by timestamp 
        'u'     Custom pipeline to compress and concatenate
        'm'     Create multi-view mosaic video
        'gpu'   Check for hardware acceleration
        'q'     Quit
            '''

            print(help)

            choice = input("\n(CPU mode) How can I help you: ")
        
        elif "acc_main" in choice:
            reset_terminal(width, height)

            # header
            print("#"*width + "\n")
            print("MIT License Copyright (c) 2022 GuillermoHidalgoGadea.com\n".center(width))
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
        'c'     Compress video with h265/h264
        'a'     Append or Concatenate multiple files
        's'     Split or Trim files by timestamp 
        'u'     Custom pipeline to compress and concatenate
        'm'     Create multi-view mosaic video
        'gpu'   Check for hardware acceleration
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
            if "y" in gpu_use:
                choice = 'acc_main'
            else:
                choice = 'main'
            
        elif choice.startswith("c"):
            # start compression
            print("\nStart compression with ffmpeg... \n")
            if "y" not in gpu_use:
                encoder = input("\n(CPU mode) Choose video encoder [h264/h265]: ")
                if "4" in encoder:
                    compress_h264()
                    input("\nCompressing ended!\n")
                    # reset while loop
                    choice = 'main'
                elif "5" in encoder:
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
            if "y" in gpu_use:
                choice = 'acc_main'
            else:
                choice = 'main'
            
        elif choice.startswith("s"):
            print("\nStart trimming videos in ffmpeg... \n")
            if "y" not in gpu_use:
                try:
                    trim_split_h265()
                    input("\nTrimming ended!\n")
                    # reset while loop
                    choice = 'main'
                except:
                    input("\nTrimming ended!\n")
                    # reset while loop
                    choice = 'main'
            else:
                try:
                    trim_split_hevc_nvenc()
                    input("\nTrimming ended!\n")
                    # reset while loop
                    choice = 'acc_main'
                except:
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
                the_usual_h265()
                input("\nPipeline ended!\n")
                # reset while loop
                choice = 'acc_main'

        elif choice.startswith("m"):
            print("\nStart creating mosaic video... \n")
            if "y" not in gpu_use:
                mosaic_video()
                input("\nMosaic video created!\n")
                # reset while loop
                choice = 'main'
            else:
                mosaic_video()
                input("\nMosaic video created!\n")
                # reset while loop
                choice = 'acc_main'
            
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
