import os
import time
import psutil

filename = "Ragnarok.ark"


batch_file = "versiontrigger.bat"
batch_file_contents = """
@echo off
setlocal enableextensions

set "versionNumFile=versionNum"
set "sourceFile=Ragnarok.ark"
set "destinationFolder=Versions"

rem check if versionNum file exists, if not create it with value 1
if not exist "%versionNumFile%" (
    echo 1 > "%versionNumFile%"
)

rem check if destination folder exists, if not create it
if not exist "%destinationFolder%" (
    mkdir "%destinationFolder%"
)

rem read version number from file
set /p versionNum=<%versionNumFile%

rem increment version number
set /a versionNum+=1

rem update version number in file
echo %versionNum% > "%versionNumFile%"

rem construct destination file name
set "destinationFile=%destinationFolder%\Ragnarok_v%versionNum%.ark"

rem copy file
copy "%sourceFile%" "%destinationFile%"

rem confirm file copy
echo File "%sourceFile%" was copied to "%destinationFile%"
"""

# check if the batch file already exists
if not os.path.exists(batch_file):
    with open(batch_file, "w") as f:
        f.write(batch_file_contents)
        print(f"{batch_file} created.")
else:
    print(f"{batch_file} already exists.")


# get the current file's modified time
current_mtime = os.path.getmtime(filename)

while True:
    # check if the process is running
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
            if pinfo['name'] == "ShooterGame.exe":
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    else:
        # process not found, so exit the script
        print("ShooterGame.exe not found STOPPING")
        break
    # check if the file's modified time has changed
    new_mtime = os.path.getmtime(filename)
    if new_mtime != current_mtime:
        current_mtime = new_mtime
        # run the batch file
        os.system(batch_file)
    # sleep for 5 seconds before checking again
    time.sleep(5)