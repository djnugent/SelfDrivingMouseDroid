import json
import os
import shutil, sys

directory = "/remote/rs/ecpeprime/training_data"
modelDirectory = "/remote/rs/ecpeprime/pretrained_models"

print("Updating")
for subdir, dirs, files in os.walk(modelDirectory):
   for file in files:
      if file == "metadata.txt":
         with open(os.path.join(subdir, file), "r") as metadata_file:
            data = subdir.split('/')
            print(str(data[5]))
            try: 
               metadata = json.load(metadata_file)
               print(metadata['name'])
               metadata['date'] = data[5]
            except:
               print("opening failed")
         with open(os.path.join(subdir, file), "w") as metadata_file:
            try:
               print(metadata['date'])
               metadata_file.seek(0, 0)
               json.dump(metadata, metadata_file)
               metadata_file.truncate()
            except: 
               print("writing failed")


