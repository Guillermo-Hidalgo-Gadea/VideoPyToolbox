# VideoPyToolbox
Play, compress, trim and concatenate videos in python using FFmpeg

## What is VideoPyToolbox?
This Toolbox is a python wrapper of a bunch of useful ffmpeg commands to play, compress and edit videos using ffmpeg.
Many video recordings in computer vision are not optimized for conventional media players due to large uncompressed sizes or incompatible video codecs (see [here](https://gitlab.ruhr-uni-bochum.de/ikn/syncflir) for such a video recording tool). FFplay can easily open video files with several codecs and play them frame by frame.
When it comes to video compression, FFmpeg can be challenging to use over command line, specially in batch processing. This toolbox allows you to run pre-defined ffmpeg commands with a few mouse clicks in Tk interfaces and interactive keyboard inputs right from the terminal.

## How to use VideoPyToolbox
The Toolbox is built as an interactive terminal prompt to guide you step by step through the process of concatenating, compressing, spliting and playing videos. You can either use the `VideoPyToolbox.py` script in your IDE, or run it from the terminal. The dist directory contains a pre-compiled executable `VideoPyToolbox.exe` for Windows. 

## Features
Video compression is set to `h.264` and `h.265`, but could be expanded in future releases. The trim/split function to extract video snippets between timestamps needs to transcode the video (h.265 cfr 0) to achieve "frame-accurate" splits. This may take a while. Lossless splits are not accurate if the exact timestamp does not contain a keyframe, which result in timeshifts of up to several seconds (depending on framerate).      

## Next release
* enhanced batch processing for trim/split
* choice between losless and re-encoded trim/split
* side-by-vide video player to check synchronizity
* choose compression codecs
* tbd
