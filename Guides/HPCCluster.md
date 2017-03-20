## How to use the HPC Cluster
The HPC Cluster is just what it sounds like; a collection of high performance computers called partitions. Some partitions have nice CPUs and some have nice GPUs. We care about the partitions with GPUs. There are 4 partitions with a *K20 Kepler 5GB GPU*. Partitions can be used interactively from the cluster manager or batch jobs can be submitted. Interactive mode is good for testing, but batch jobs are good for when all partitions are in use or when running long jobs. A partition can only handle a single job at a time(whether it's interactive or a batch job)

1. ssh into cluster manager `ssh net-id@duh310-06.ece.iastate.edu`
  * Make sure you are on the iastate VPN if not on campus
  * Replace net-id with your id
2. Install keras/tensorflow/opencv locally run, `pip install --user opencv-python keras tensorflow-gpu`
  * Only need to install once.
  * Note: this installs on your 5gb HPC private user directory, not your MyFiles(Udrive)
3. start an interactive session on a GPU partition, run `salloc -p gpu`
4. load the cuda module, run `module load cuda`
   * verify that a GPU exists, run  `nvidia-smi` There is no reason it shouldn't but...
5. Run your python code!!
6. exit the gpu parition `exit`
7. exit the ssh session `exit`

**Note:** `salloc` starts an interactive session. The proper way to use a partition is to create a batch job which can be scheduled and run in the background. This is respectful to others using the cluster and allows you to use it during busy times. See [this](http://www.hpc.iastate.edu/guides/classroom-hpc-cluster/managing-jobs-using-slurm-workload-manager) and check out there SLURM script generator for creating batch jobs.
