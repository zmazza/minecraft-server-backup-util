"""
Owner: Zac Mazza
Date: 27 MAR 2021

Purpose: A utility for backing up a Spigot minecraft server on a Linux machine, zipping the required folders, and loading
that zip into a destination directory.
"""

import shutil
import zipfile
import os
from pathlib import Path
import time


def zip_dir(directory, zipname):
    """
    Compresses a directory (ZIP file).
    """
    if os.path.exists(directory):
        outZipFile = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)

        # The root directory within the ZIP file. 
        rootdir = os.path.basename(directory)

        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:

                # Write the file named filename to the archive,
                # giving it the archive name 'arcname.'
                filepath = os.path.join(dirpath, filename)
                parentpath = os.path.relpath(filepath, directory)
                arcname = os.path.join(rootdir, parentpath)

                outZipFile.write(filepath, arcname)
    
    outZipFile.close()


print("Script started...")

# Directories
root_src_dir = "/home/pi/minecraft-server"
root_tmp_dir = "/tmp/tmp_minecraft_backups"
root_dst_dir = "/home/pi/minecraft-backups"

path = Path('/tmp/tmp_minecraft_backups')
if os.path.isdir(path):
    shutil.rmtree(path)

source = os.listdir(root_src_dir)
files_to_backup = ['banned-ips.json', 'banned-players.json', 'ops.json', 'server.properties']
directories_to_backup = ['plugins', 'world', 'world_nether', 'world_the_end']

for directories in source:
    if(directories in directories_to_backup):
        directory_to_move = root_src_dir + "/" + directories
        new_directory = root_tmp_dir + "/" + directories
        print("Copying {} to {}...".format(directory_to_move, new_directory))
        
        shutil.copytree(directory_to_move, new_directory)

for files in source:
    if(files in files_to_backup):
        file_to_move = os.path.join(root_src_dir, files)
        new_file_name = os.path.join(root_tmp_dir, files)
        print("Copying {} to {}...".format(file_to_move, new_file_name))
        if(os.path.isfile(file_to_move) != True):
            print("File does not exist.")
        else:
            shutil.copy(file_to_move, new_file_name)      
    
# Zip the remaining files
timestr = time.strftime("%Y%m%d-%H%M%S")
zip_filename = timestr + "_minecraft_backup.zip"

print("Zipping directory...")
zip_dir(root_tmp_dir, zip_filename)

time.sleep(2)

# Move the zip file to the backup directory
print("Moving zipped file...")
shutil.move("" + zip_filename, root_dst_dir)

# Delete the temporary directory
print("Removing temp dir...")
shutil.rmtree(root_tmp_dir)
time.sleep(2)

# Delete the OLDEST zip over 2 backups
print("Deleting oldest backup...")
backups = os.listdir(root_dst_dir)
while len(os.listdir(root_dst_dir)) > 2:
    backups = os.listdir(root_dst_dir)
    file_to_remove = backups[0]
    os.remove(os.path.join(root_dst_dir, file_to_remove))
    time.sleep(2)