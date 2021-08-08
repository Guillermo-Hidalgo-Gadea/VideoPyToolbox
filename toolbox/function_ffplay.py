'''
====================================================================================================
Helper function for the VideoPyToolbox

MIT License Copyright (c) 2021 GuillermoHidalgoGadea.com

Sourcecode: https://github.com/Guillermo-Hidalgo-Gadea/VideoPyToolbox
====================================================================================================
'''

import os
from tkinter import filedialog

def ffplay():
    '''
    Video player with ffplay and mosaic display
    '''
    # Choose Video File from Dialog Box
    
    videofiles = filedialog.askopenfilenames(title='Choose the Video Files you want to play')
    if not videofiles:
        return
    
    # common standard scaling
    std_scale = '1920:1080'

    # get number of input videos
    if len(videofiles) == 1:

        # list video files
        video1 = f"\"{videofiles[0]}\""
        # Note that Win paths may contain colon as in D:/... add '' to filename 

        # add timestamp
        ffplay_timecode = "\"drawtext=fontfile=Arial.ttf: text='%{pts\:hms} Frame\: %{frame_num}': x=(w-tw)/1.1: y=h-(2*lh): fontcolor=black: fontsize=50: box=1: boxcolor=white: boxborderw=5\""
        ffplay_command = f"ffplay -x 1200 -vf {ffplay_timecode} {video1}"
        
        # play video
        os.system(ffplay_command)

    elif len(videofiles) == 2:

        # list video files
        video1 = f"\"{videofiles[0]}\""
        video2 = f"\"{videofiles[1]}\""

        # 2x1 grid
        ffplay_grid =  f"\"movie={video1},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v1]; movie={video2},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v2];[v1][v2]hstack\""
        
        # add timestamp
        ffplay_timecode = "\"drawtext=fontfile=Arial.ttf: text='%{pts\:hms} Frame\: %{frame_num}': x=(w-tw)/1.1: y=h-(2*lh): fontcolor=black: fontsize=50: box=1: boxcolor=white: boxborderw=5\""
        ffplay_command = f"ffplay -x 1200 -f lavfi -i {ffplay_grid} -vf {ffplay_timecode}"

        # play mosaic
        os.system(ffplay_command)

    elif len(videofiles) == 3:

        # list video files
        video1 = videofiles[0]
        video2 = videofiles[1]
        video3 = videofiles[2]

        # 2x2 grid with padding in last cell
        ffplay_grid = f"\"movie={video1},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v1]; movie={video2},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v2]; movie={video3},scale={std_scale}:force_original_aspect_ratio=decrease,pad=iw*2:ih:0:-1:color=black[v3]; [v1][v2]hstack[top]; [top][v3]vstack\""
        
        # add timestamp
        ffplay_timecode = "\"drawtext=fontfile=Arial.ttf: text='%{pts\:hms} Frame\: %{frame_num}': x=(w-tw)/1.1: y=h-(2*lh): fontcolor=black: fontsize=50: box=1: boxcolor=white: boxborderw=5\""
        ffplay_command = f"ffplay -x 1200 -f lavfi -i {ffplay_grid} -vf {ffplay_timecode}"

        # play mosaic
        os.system(ffplay_command)

    elif len(videofiles) == 4:

        # list video files
        video1 = videofiles[0]
        video2 = videofiles[1]
        video3 = videofiles[2]
        video4 = videofiles[3]

        # 2x2 grid
        ffplay_grid = f"\"movie={video1},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v1]; movie={video2},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v2]; movie={video3},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v3]; movie={video4},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v4]; [v1][v2]hstack[top]; [v3][v4]hstack[bottom]; [top][bottom]vstack\""
        
        # add timestamp
        ffplay_timecode = "\"drawtext=fontfile=Arial.ttf: text='%{pts\:hms} Frame\: %{frame_num}': x=(w-tw)/1.1: y=h-(2*lh): fontcolor=black: fontsize=50: box=1: boxcolor=white: boxborderw=5\""
        ffplay_command = f"ffplay -x 1200 -f lavfi -i {ffplay_grid} -vf {ffplay_timecode}"

        # play mosaic
        os.system(ffplay_command)

    elif len(videofiles) == 5:
        
        # list video files
        video1 = videofiles[0]
        video2 = videofiles[1]
        video3 = videofiles[2]
        video4 = videofiles[3]
        video5 = videofiles[4]

        # 3x2 grid with padding in last cell
        ffplay_grid = f"\"movie={video1},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v1]; movie={video2},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v2]; movie={video3},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v3]; movie={video4},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v4]; movie={video5},scale={std_scale}:force_original_aspect_ratio=decrease,pad=iw*2:ih:0:-1:color=black[v5]; [v1][v2]hstack[top1]; [top1][v3]hstack[top]; [v4][v5]hstack[bottom]; [top][bottom]vstack\""
        
        # add timestamp
        ffplay_timecode = "\"drawtext=fontfile=Arial.ttf: text='%{pts\:hms} Frame\: %{frame_num}': x=(w-tw)/1.1: y=h-(2*lh): fontcolor=black: fontsize=50: box=1: boxcolor=white: boxborderw=5\""
        ffplay_command = f"ffplay -x 1200 -f lavfi -i {ffplay_grid} -vf {ffplay_timecode}"

        # play mosaic
        os.system(ffplay_command)

    elif len(videofiles) == 6:
        # grid 3x2
        # list video files
        video1 = videofiles[0]
        video2 = videofiles[1]
        video3 = videofiles[2]
        video4 = videofiles[3]
        video5 = videofiles[4]
        video6 = videofiles[5]

        # 3x2 grid with padding in last cell
        ffplay_grid = f"\"movie={video1},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v1]; movie={video2},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v2]; movie={video3},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v3]; movie={video4},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v4]; movie={video5},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v5]; movie={video6},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v6]; [v1][v2]hstack[top1]; [top1][v3]hstack[top]; [v4][v5]hstack[bottom1]; [bottom1][v6]hstack[bottom]; [top][bottom]vstack\""
        
        # add timestamp
        ffplay_timecode = "\"drawtext=fontfile=Arial.ttf: text='%{pts\:hms} Frame\: %{frame_num}': x=(w-tw)/1.1: y=h-(2*lh): fontcolor=black: fontsize=50: box=1: boxcolor=white: boxborderw=5\""
        ffplay_command = f"ffplay -x 1200 -f lavfi -i {ffplay_grid} -vf {ffplay_timecode}"

        # play mosaic
        os.system(ffplay_command)

    elif len(videofiles) == 7:
        # grid 3x2
        # list video files
        video1 = videofiles[0]
        video2 = videofiles[1]
        video3 = videofiles[2]
        video4 = videofiles[3]
        video5 = videofiles[4]
        video6 = videofiles[5]
        video7 = videofiles[6]

        # 3x3 grid with padding in last two cells
        ffplay_grid = f"\"movie={video1},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v1]; movie={video2},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v2]; movie={video3},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v3]; movie={video4},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v4]; movie={video5},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v5]; movie={video6},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v6]; movie={video7},scale={std_scale}:force_original_aspect_ratio=decrease,pad=iw*3:ih:0:-1:color=black[v7]; [v1][v2]hstack[top1]; [top1][v3]hstack[top]; [v4][v5]hstack[mid1]; [mid1][v6]hstack[mid]; [top][mid]vstack[up]; [up][v7]vstack\""
        
        # add timestamp
        ffplay_timecode = "\"drawtext=fontfile=Arial.ttf: text='%{pts\:hms} Frame\: %{frame_num}': x=(w-tw)/1.1: y=h-(2*lh): fontcolor=black: fontsize=50: box=1: boxcolor=white: boxborderw=5\""
        ffplay_command = f"ffplay -x 1200 -f lavfi -i {ffplay_grid} -vf {ffplay_timecode}"

        # play mosaic
        os.system(ffplay_command)

    elif len(videofiles) == 8:
        # grid 3x2
        # list video files
        video1 = videofiles[0]
        video2 = videofiles[1]
        video3 = videofiles[2]
        video4 = videofiles[3]
        video5 = videofiles[4]
        video6 = videofiles[5]
        video7 = videofiles[6]
        video8 = videofiles[7]

        # 3x3 grid with padding in last cell
        ffplay_grid = f"\"movie={video1},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v1]; movie={video2},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v2]; movie={video3},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v3]; movie={video4},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v4]; movie={video5},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v5]; movie={video6},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v6]; movie={video7},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v7]; movie={video8},scale={std_scale}:force_original_aspect_ratio=decrease,pad=iw*2:ih:0:-1:color=black[v8]; [v1][v2]hstack[top1]; [top1][v3]hstack[top]; [v4][v5]hstack[mid1]; [mid1][v6]hstack[mid]; [v7][v8]hstack[bottom]; [top][mid]vstack[up]; [up][bottom]vstack\""
        
        # add timestamp
        ffplay_timecode = "\"drawtext=fontfile=Arial.ttf: text='%{pts\:hms} Frame\: %{frame_num}': x=(w-tw)/1.1: y=h-(2*lh): fontcolor=black: fontsize=50: box=1: boxcolor=white: boxborderw=5\""
        ffplay_command = f"ffplay -x 1200 -f lavfi -i {ffplay_grid} -vf {ffplay_timecode}"

        # play mosaic
        os.system(ffplay_command)

    elif len(videofiles) == 9:
        # grid 3x2
        # list video files
        video1 = videofiles[0]
        video2 = videofiles[1]
        video3 = videofiles[2]
        video4 = videofiles[3]
        video5 = videofiles[4]
        video6 = videofiles[5]
        video7 = videofiles[6]
        video8 = videofiles[7]
        video9 = videofiles[8]

        # 3x3 grid
        ffplay_grid = f"\"movie={video1},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v1]; movie={video2},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v2]; movie={video3},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v3]; movie={video4},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v4]; movie={video5},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v5]; movie={video6},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v6]; movie={video7},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v7]; movie={video8},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v8]; movie={video9},scale={std_scale}:force_original_aspect_ratio=decrease,pad={std_scale}:-1:-1:color=black[v9]; [v1][v2]hstack[top1]; [top1][v3]hstack[top]; [v4][v5]hstack[mid1]; [mid1][v6]hstack[mid]; [v7][v8]hstack[bottom1]; [bottom1][v9]hstack[bottom]; [top][mid]vstack[up]; [up][bottom]vstack\""
        
        # add timestamp
        ffplay_timecode = "\"drawtext=fontfile=Arial.ttf: text='%{pts\:hms} Frame\: %{frame_num}': x=(w-tw)/1.1: y=h-(2*lh): fontcolor=black: fontsize=50: box=1: boxcolor=white: boxborderw=5\""
        ffplay_command = f"ffplay -x 1200 -f lavfi -i {ffplay_grid} -vf {ffplay_timecode}"

        # play mosaic
        os.system(ffplay_command)

    else:
        input(f"Sorry, {len(videofiles)} videos are too many. Try with up to 6 files.")
        return
