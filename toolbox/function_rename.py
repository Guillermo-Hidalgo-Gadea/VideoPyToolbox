'''
====================================================================================================
Helper function for the VideoPyToolbox

MIT License Copyright (c) 2021 GuillermoHidalgoGadea.com

Sourcecode: https://github.com/Guillermo-Hidalgo-Gadea/VideoPyToolbox
====================================================================================================
'''

import os                           # paths and terminal commands
from tkinter import filedialog      # interactive interface to selet files 

def batch_rename():
    '''
    This function reads a list of files and appends/prepends string filename 
    '''

    choice = 'y'
    
    while True:
        if choice == 'y':
            # choose batch of files to rename
            batch = list(filedialog.askopenfilenames(title='Choose Video Batch to rename'))
            dir_list = [os.path.dirname(file)for file in batch]
            name_list = [os.path.basename(file).split('.')[0] for file in batch]
            suffix_list = [os.path.basename(file).split('.')[1] for file in batch]

            # ask for 
            prepend = input(f"Prepend string for videos ..._{name_list[0]}: ")
            append = input(f"Append string for videos {name_list[0]}_... : ")

            #edit new file names
            newnames = [prepend+'_'+name+'_'+append+'.'+suffix for name, suffix in zip(name_list, suffix_list)]
            newbatch = [dir+'/'+file for dir,file in zip(dir_list,newnames)]

            # rename files
            for i in range(len(batch)):
                os.rename(batch[i], newbatch[i])

            # reset loop
            choice = input(f"Rename another Video Batch [y/N]: ")

        else:
            break