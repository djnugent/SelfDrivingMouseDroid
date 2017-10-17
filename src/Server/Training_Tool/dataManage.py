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
                with open(file) as metadata_file:
                    data = json.load(data_file)

    return data   


def writeModelData(modelData)
    open(os.path.join(directory, date, modelData["modelName"+.txt]), 'w') as f:
    json.dump(modelData, f)


   
def deleteDataset(dataset):
    shutil.rmtree(os.path.join(directory, dataset), ignore_errors=False, onerror=None)
