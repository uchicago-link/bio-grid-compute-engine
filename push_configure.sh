#!/bin/sh
################################################################################
#
# push_configure.sh
#
#   - Automates the configuration of glusterFS on the master and worker nodes
#   - Downloads the sample distributed work example files to the shared directory
#
#
################################################################################

declare SHARED_DIRECTORY="/home/biogrid-shared/"
declare SHARED_VOLUME="biogrid-mm:/biogrid-volume"

################################################################################
# Get a list of all the instances for later use
instances=`gcutil listinstances | grep biogrid | awk '{print $2}'`
instance_master=`gcutil listinstances | grep biogrid-mm | awk '{print $2}'`
instance_workers=`gcutil listinstances | grep biogrid-ww | awk '{print $2}'`


################################################################################
# Send listen for peers to master
# gcutil listinstances | grep ww | awk '{print "gcutil ssh "$2" \x27sudo gluster peer probe "$2" \x27"}'
for instance in $instance_workers; do
    echo "### Instance: "$instance
    gcutil ssh $instance_master "sudo gluster peer probe $instance"
done


################################################################################
# Mount the shared directory on all instances
#  - sudo mount -t glusterfs biogrid-mm:/biogrid-volume /home/biogrid-shared/
#   gcutil listinstances | grep biogrid | awk -v dir="$SHARED_DIRECTORY" -v vol="$SHARED_VOLUME" '{print "gcutil ssh "$2" \x27sudo mount -t glusterfs "vol,dir" \x27 &"}'
for instance in $instances; do
    echo "### Instance: "$instance
    gcutil ssh $instance "sudo mount -t glusterfs $SHARED_VOLUME $SHARED_DIRECTORY"
done


################################################################################
# Download sample scripts to the shared directory
#  - On master
files_to_download="https://gist.githubusercontent.com/tabinks/9d0a9a382ad5bba46fbc/raw/f7a3deac259bc3031e4f8fc1fe57050269dbceef/myApplication.py \
    https://gist.githubusercontent.com/tabinks/8b599ff89ce3c06ebdf6/raw/5bfdb0645672350aa36681c58102d6a9d915927f/batchSubmit.py \
    https://gist.githubusercontent.com/tabinks/4383ea8b12b087386c6f/raw/b11eb178c038159752a88b3d0f4ed038d439b7b1/cleanupBatchSubmit.sh"

for file in $files_to_download; do
    echo "## Pushing file: "$file
    gcutil ssh biogrid-mm "wget $file -P $SHARED_DIRECTORY"
done




