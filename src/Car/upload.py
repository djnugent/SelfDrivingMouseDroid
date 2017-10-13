import os
import re
import shutil

## This script will upload training data from odroid to the remote network drive
## It will delete runs locally as it uploads them

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


# Regex for extracting batchsize from meta data
p = re.compile("Batch Size: (?:\d*)?\d+")


# List runs
path, runs, files = os.walk(local_directory).__next__()
print(">> Found {} runs".format(len(runs)))

# Iterate through each run
for i,run in enumerate(runs):
	print(">> Run",i)
	# Extract batch size from metadata
	metadata = open(local_directory + "/" + run + "/metadata.txt","r")
	line = metadata.read()
	metadata.close()
	batch_size = int(p.search(line).group().replace("Batch Size: ",""))

	# Detect batches in each run
	path, batches, files = os.walk(local_directory + "/" + run).__next__()
	print("   --Found {} batches".format(len(batches)))
	
	for j,batch in enumerate(batches):
		# Check for complete batch
		path, dirs, files = os.walk(local_directory + "/" + run + "/" + batch).__next__()
		# valid batch, move to server
		if len(files) - 1 == batch_size:	
			print("   --Uploading batch {}".format(j))
			# mv batch
			copy_all(local_directory + "/" + run + "/" + batch, remote_directory + "/" + run + "/" + batch)
		# incomplete batch, skip
		else:
			print("   --Batch {} incomplete. Skipping".format(j))


	# transfer meta data
	shutil.copy(local_directory + "/" + run + "/metadata.txt", remote_directory + "/" + run + "/metadata.txt")
	
	# delete run from local directory after successful transfer
	print("   --Run {} transfer complete. Removing".format(i))
	shutil.rmtree(local_directory + "/" + run)


print("Upload complete")
			

