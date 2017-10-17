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
                f = open(os.path.join(subdir, file), 'r')
                alltext = f.read()
                entries = alltext.split("~")
                json_entry = {"recordedBy":entries[0],
                              "location":entries[1],
                              "batch_size":entries[2],
                              "obstacles":entries[3],
                              "pedestrians":entries[4],
                              "tags":entries[5],
                              "notes":entries[6],
                              "date":entries[7]}
                data.append(json_entry)
    #print(json.dumps(data))
    return json.dumps(data)   


def writeModelData(modelData)
    open(os.path.join(directory, date, modelData["modelName"+.txt]), 'w') as f:
    json.dump(modelData, f)


   
def deleteDataset(dataset):
    shutil.rmtree(os.path.join(directory, dataset), ignore_errors=False, onerror=None)
