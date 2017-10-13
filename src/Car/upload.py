
# TODO recursive move files and delete after transfer

import os
import re

# Regex for extracting batchsize from meta data
p = re.compile("Batch Size: (?:\d*)?\d+")


directory = '/remote/rs/ecpeprime/training_data'
local_directory = '/home/odroid/training_data_tmp'

# List runs
path, runs, files = os.walk(local_directory).__next__()
print(">> Found {} runs".format(len(runs)))

# Iterate through each run
for i,run in enumerate(runs):
	print(">> Run",i)
	# Extract batch size from metadata
	metadata = open(local_directory + "/" + run + "/metadata.txt","r")
	line = metadata.read()
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
		# incomplete batch, skip
		else:
			print("   --Batch {} incomplete. Skipping".format(j))

	# delete run from local directory after successful transfer
	print("   --Run {} transfer complete. Removing".format(i))

print("Upload complete")
			

