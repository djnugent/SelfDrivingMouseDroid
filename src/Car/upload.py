# todo dont upload incomplete batches
# delete after upload

directory = '/remote/rs/ecpeprime/training_data'

    # Remove incomplete batch
    if (frame_count < batch_size - 1):
        shutil.rmtree(directory + "/" + run_name + "/" + str(batch_num))
