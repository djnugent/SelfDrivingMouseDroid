import os
import re
import shutil
import time

## This script will upload training data from odroid to the remote network drive
## It will delete runs locally as it uploads them
## Uploads PARTIAL and FULL batches

local_directory = '/home/odroid/training_data_tmp'
remote_directory = '/remote/rs/ecpeprime/training_data'

# Recursive copy
def copy_all(src,dst):
	for src_dir, dirs, files in os.walk(src):
		dst_dir = src_dir.replace(src, dst)
		if not os.path.exists(dst_dir):
		    os.makedirs(dst_dir, exist_ok=True)
		for file_ in files:
		    src_file = os.path.join(src_dir, file_)
		    dst_file = os.path.join(dst_dir, file_)
		    if os.path.exists(dst_file):
		        os.remove(dst_file)
		    shutil.copy(src_file, dst_dir)



# List runs
path, runs, files = os.walk(local_directory).__next__()
print(">> Found {} runs".format(len(runs)))

# Time upload
start = time.time()
num_batches = 0
num_samples = 0

# Iterate through each run
for i,run in enumerate(runs):
	print(">> Run",i)
	# Detect batches in each run
	path, batches, files = os.walk(local_directory + "/" + run).__next__()
	print("   --Found {} batches".format(len(batches)))

	# Iterate throught each batch
	for j,batch in enumerate(batches):
		# get batch size
		path, dirs, files = os.walk(local_directory + "/" + run + "/" + batch).__next__()
		batch_size = len(files) - 1
		print("   --Uploading batch {} with {} samples".format(batch,batch_size))
		# transfer batch to remote directory
		copy_all(local_directory + "/" + run + "/" + batch, remote_directory + "/" + run + "/" + batch)

		# keep track of uploads
		num_samples += batch_size		
		num_batches += 1
		
	# transfer meta data
	if os.path.isdir(remote_directory + "/" + run):
		shutil.copy(local_directory + "/" + run + "/metadata.txt", remote_directory + "/" + run + "/metadata.txt")
	
	# delete run from local directory after successful transfer
	print("   --Run {} transfer complete. Removing".format(i))
	shutil.rmtree(local_directory + "/" + run)



# Stats
upload_time = round((time.time() - start)/60,2) # mins
avg_batch_time = round(upload_time / num_batches,2) # mins
avg_sample_time = round(upload_time * 60 / num_samples,1) # sec
samples_per_batch = round(num_samples * 1.0/num_batches,2)
print(">> Upload complete: {} min".format(upload_time))
print("   --Transfered {} batches".format(num_batches))
print("   --Transfered {} samples".format(num_samples))
print("   --Average samples per batch: {}".format(samples_per_batch))
print("   --Average Batch upload time: {} min".format(avg_batch_time))
print("   --Average Sample upload time: {} sec".format(avg_sample_time))
			

