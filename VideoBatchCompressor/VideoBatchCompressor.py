##########################################################################################
#                                   VideoBatchCompression
# A python script to scrap, concatenate and compress video snippets from syncFLIR & TheBeehive
#                           (C) 2023 GuillermoHidalgoGadea.com
##########################################################################################

import numpy, os, sys, yaml, time
from natsort import ns, natsorted


def getConfigpath():
    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    print(f"Looking for config.yaml file in {application_path}")

    configpath = os.path.join(application_path, 'config.yaml')
    print(f'Found config.yaml file {configpath}')
    
    return configpath

def readConfig(configpath):
    # read config file
    print('Reading configuration paramters...')

    '''
    CONFIG.YAML SHOUD HAVE THIS FORM
    sourcedir = r'D:\ForagingPlatformsArena_local2\DataDump'
    outputdir = r'D:\ForagingPlatformsArena_local2\Behavior'
    projectname = 'ForagingPlatforms'
    extension = '.avi'
    crf = 12

    cam_assignement = { '20323040': 'camA',
                        '20323042': 'camB', 
                        '20323043': 'camC',
                        '20323044': 'camD', 
                        '20323049': 'camE', 
                        '20323052': 'camF'}
    '''
    with open(configpath) as f:
        my_dict = yaml.safe_load(f)
    
    # extract compression parameters 
    sourcedir = my_dict['sourcedir']
    print(f'sourcedir: {sourcedir}')
    outputdir = my_dict['outputdir']
    print(f'outputdir: {outputdir}')
    projectname = my_dict['projectname']
    print(f'projectname: {projectname}')
    extension = my_dict['extension']
    print(f'video extension: {extension}')
    crf = my_dict['crf']
    print(f'compression crf: {crf}')
    cam_assignement = my_dict['cam_assignement']
    print(f'camera assignement: {cam_assignement}')
    time.sleep(5)
    
    return sourcedir, outputdir, projectname, extension, crf, cam_assignement

def existing_files(outputfile, outputdir):
    '''
    Check if the output file already exists, 
    rise a flag and skip the compression job.
    '''
    existing = [os.path.join(outputdir, file) for file in os.listdir(outputdir)]
    flag = False
    if outputfile in existing:
        flag = True
    
    return flag

def VideoCompression(configpath):
    # read config parameters
    sourcedir, outputdir, projectname, ext, crf, cam_assignement = readConfig(configpath)

    # find all videos in source directory
    video_list = []
    print(f"Scrapping videos in {sourcedir}")
    for root, dirs, files in os.walk(sourcedir):
        videos = [os.path.join(root, file) for file in files if ext in file]
        video_list.append(videos)

    flatten = [item for sublist in video_list for item in sublist]
    filenames = list(natsorted(flatten, alg=ns.IGNORECASE))
    print(f"Found {len(filenames)} video snippets...")
    # match videos snippets by camera and session
    session = []
    cams = []
    snip = []

    for file in filenames:
        session.append(os.path.basename(os.path.dirname(file)))
        cams.append(os.path.basename(file).split('_')[2])
        snip.append(os.path.basename(file).split('_')[-1].split('-')[0])
    
    session = set(session)
    cams = set(cams)
    snip = set(snip)

    # group files
    grouped = []
    for recording in session:
        for cam in cams:
            snippets = [file for file in filenames if cam in file and recording in file]
            if snippets in grouped:
                pass
            elif bool(snippets): # append only non empty lists
                grouped.append(snippets)
            else:
                pass

    # create matching output files
    concats = []
    
    for snippets in grouped:
        try:
            name = os.path.basename(os.path.dirname(snippets[0]))
            serial = os.path.basename(snippets[0]).split('_')[2]
        except:
            name = 'X_X_X_X'
            serial = None

        # assign camera ID
        if serial:
            cam = cam_assignement[serial]
        else:
            cam = 'camX'
            print(f'Error assigning camera ID for file {name}')
        
        output = [f'h265_crf{crf}_' + name.split('_')[0] + '_' + projectname + '_' + name.split('_')[2] + '_' + cam +'.mp4'] * len(snippets)

        # append or create concatenation dataset
        try:
            concats = numpy.vstack((concats, numpy.column_stack((snippets, output))))
        except:
            concats = numpy.column_stack((snippets, output))

    # loop over output files and create compression job
    for outputfile in numpy.unique(concats[:,1]):
        filenames = concats[concats[:,1]==outputfile][:,0]

        # set output directory
        output = os.path.join(outputdir, outputfile)

        # check if file already exists in outputdir
        flag = existing_files(outputfile, outputdir)
        
        if flag:
            print(f'File {outputfile} already exists, skipping!')
            pass
        else:
            print(f'Compressing Video {outputfile} from following files:')
            print(filenames)

            # write mylist.txt for ffmpeg
            ffmpegfile = sourcedir + "/ffmpeg_concat_list.txt"
            with open(ffmpegfile, "w+") as textfile:
                for element in filenames:
                    _, name = os.path.split(element)
                    textfile.write("file " +"'"+ element + "'\n")
                textfile.close()
            
            # create ffmpeg command
            ffmpeg_command = f'ffmpeg -y -f concat -safe 0 -i {ffmpegfile} -an -dn -vcodec libx265 -crf {crf} {output}'
            os.system(ffmpeg_command)
            os.remove(ffmpegfile)

    return

## ENTRY POINT ##
if __name__ == '__main__':
    
    VideoCompression(getConfigpath())