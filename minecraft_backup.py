"""
Owner: Zac Mazza
Date: 27 MAR 2021
Purpose: A utility for backing up a Spigot minecraft server on a Linux machine,
zipping the required folders, and loading
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
        out_zip_file = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)

        # The root directory within the ZIP file.
        rootdir = os.path.basename(directory)

        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:

                # Write the file named filename to the archive,
                # giving it the archive name 'arcname.'
                filepath = os.path.join(dirpath, filename)
                parentpath = os.path.relpath(filepath, directory)
                arcname = os.path.join(rootdir, parentpath)

                out_zip_file.write(filepath, arcname)

    out_zip_file.close()


print("Script started...")

# Directories
ROOT_SRC_DIR = "/home/pi/minecraft-server"
ROOT_TMP_DIR = "/tmp/tmp_minecraft_backups"
ROOT_DST_DIR = "/home/pi/minecraft-backups"

path = Path('/tmp/tmp_minecraft_backups')
if os.path.isdir(path):
    shutil.rmtree(path)

source = os.listdir(ROOT_SRC_DIR)
files_to_backup = [
    'banned-ips.json',
    'banned-players.json',
    'ops.json',
    'server.properties']
directories_to_backup = ['plugins', 'world', 'world_nether', 'world_the_end']

for directories in source:
    if directories in directories_to_backup:
        directory_to_move = ROOT_SRC_DIR + "/" + directories
        new_directory = ROOT_TMP_DIR + "/" + directories
        print("Copying {} to {}...".format(directory_to_move, new_directory))

        shutil.copytree(directory_to_move, new_directory)

for files in source:
    if files in files_to_backup:
        file_to_move = os.path.join(ROOT_SRC_DIR, files)
        new_file_name = os.path.join(ROOT_TMP_DIR, files)
        print("Copying {} to {}...".format(file_to_move, new_file_name))
        if os.path.isfile(file_to_move) is not True:
            print("File does not exist.")
        else:
            shutil.copy(file_to_move, new_file_name)

# Zip the remaining files
timestr = time.strftime("%Y%m%d-%H%M%S")
zip_filename = timestr + "_minecraft_backup.zip"

print("Zipping directory...")
zip_dir(ROOT_TMP_DIR, zip_filename)

time.sleep(2)

# Move the zip file to the backup directory
print("Moving zipped file...")
shutil.move("" + zip_filename, ROOT_DST_DIR)

# Delete the temporary directory
print("Removing temp dir...")
shutil.rmtree(ROOT_TMP_DIR)
time.sleep(2)

# Delete the OLDEST zip over 2 backups
print("Deleting oldest backup...")
backups = os.listdir(ROOT_DST_DIR)
while len(os.listdir(ROOT_DST_DIR)) > 2:
    backups = os.listdir(ROOT_DST_DIR)
    file_to_remove = backups[0]
    os.remove(os.path.join(ROOT_DST_DIR, file_to_remove))
    time.sleep(2)