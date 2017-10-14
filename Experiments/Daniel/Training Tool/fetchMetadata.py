import json
import os

def fetch():
    print("Fetching Metadata")
    directory = "/remote/rs/ecpeprime"

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
    return json.dumps(data)
