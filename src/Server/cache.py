import os
import shutil, sys

tmp_directory = "/tmp/share/training_data"
storage_directory = "/remote/rs/ecpeprime/training_data"

def cacheDatasets(datasets):
    for dataset in datasets:
        dst_dir = os.path.join(tmp_directory, dataset)
        src_dir = os.path.join(storage_directory, dataset)
        print (dst_dir)
        print (src_dir)
        
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir, exist_ok=True)
        for src_dir, dirs, files in os.walk(src_dir):
            for subdir in dirs:
                dst_subdir = os.path.join(dst_dir, subdir)
                src_subdir = os.path.join(src_dir, subdir)
                print(src_subdir)

                if not os.path.exists(dst_subdir):
                    os.makedirs(dst_subdir, exist_ok=True)
                for src_subdir, subdirs, files in os.walk(src_subdir):
                    for file_ in files:
                        src_file = os.path.join(src_subdir, file_)
                        dst_file = os.path.join(dst_subdir, file_) 
                        shutil.copy(src_file, dst_subdir)
                        #print(src_file)


#datasets = ['2017-10-14_21-25-56', '2017-10-16_00-34-42']
#cacheDatasets(datasets)
