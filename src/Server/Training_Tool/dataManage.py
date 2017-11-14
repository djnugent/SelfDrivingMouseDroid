import json
import os
import shutil, sys

directory = "/remote/rs/ecpeprime/training_data"

def fetchMetadata():
    print("Fetching Metadata")

    data = [];
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file == "metadata.txt":
                with open(os.path.join(subdir, file)) as metadata_file:
                    try:
                        metadata = json.load(metadata_file)
                        #print(metadata["notes"])
                        data.append(metadata)
                    except:
                        print("Failed to add JSON for " + str(subdir))
    return data


def writeModelData(model_dir, modelData):
    with open(os.path.join(model_dir, "metadata.txt"), 'w') as f:
        json.dump(modelData, f)



def deleteDataset(dataset):
    shutil.rmtree(os.path.join(directory, dataset), ignore_errors=False, onerror=None)
