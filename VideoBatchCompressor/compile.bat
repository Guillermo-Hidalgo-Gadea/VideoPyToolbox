echo @off
call C:/Users/hidalggc/Anaconda3/Scripts/activate.bat C:/Users/hidalggc/Anaconda3
cd C:\Users\hidalggc\GitLab\the-beehive\videobatchcompression
call pyinstaller --add-binary C:\Users\hidalggc\Anaconda3\Library\bin\ffmpeg.exe;. --onefile --icon=logo.ico --version-file version.rc videobatchcompressor.py