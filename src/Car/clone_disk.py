import os
import re
import shutil
import time

## This script will backup the disk image to the remote server


local_directory = '/dev/mmcblk0'
remote_directory = '/remote/rs/ecpeprime/odroid_backups/'

## DD operation
'''sudo dd if=/dev/mmcblk0 bs=4096 conv=noerror,sync status=progress | sudo gzip -c > /remote/rs/ecpeprime/odroid_backups/2017-10-22_19-00-00/backup.img.gz'''


# Stats
upload_time = round((time.time() - start)/60,2) # mins

print(">> Upload complete: {} min".format(upload_time))

			

