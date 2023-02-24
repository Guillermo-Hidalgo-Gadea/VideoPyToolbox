echo @off
call C:/Users/hidalggc/Anaconda3/Scripts/activate.bat C:/Users/hidalggc/Anaconda3
cd C:\Users\hidalggc\GitHub\VideoPyToolbox\VideoBatchCompressor
call pyinstaller --add-binary C:\Users\hidalggc\Anaconda3\Library\bin\ffmpeg.exe;. --onefile --icon=logo.ico --version-file version.rc VideoBatchCompressor.py