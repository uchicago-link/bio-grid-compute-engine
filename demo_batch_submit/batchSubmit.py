#!/usr/bin/python                                                                                                                                                                         
import os
import datetime
import urllib2

#                                                                                                                                                                                         
QSUB_COMMAND = "qsub -cwd"
NUMBER_OF_JOBS = 40

# Load the database file over HTTP                                                                                                                                                        
response = urllib2.urlopen('https://gist.githubusercontent.com/tabinks/ff78e5b392cc5fb36af6/raw/4422a548fbd8bfbdd42a06a267c1923ce3c6ef6a/gistfile1.txt')

# Read the file and split each line into a list                                                                                                                                           
data = response.readlines()
NUMBER_OF_DATA_PER_JOB = int( (len(data)/20.0) + .5)

# Batch the list into NUMBER_OF_NODES equal parts                                                                                                                                         
batched_data = zip(*[iter(data)]*NUMBER_OF_DATA_PER_JOB)

# Create a file of the batched data that represents the                                                                                                                                   
# segment of data to be run each job                                                                                                                                                      
index = 0
for job in batched_data:
    print job
    data_file_name = "data.%d.txt" % index
    data_file = open(data_file_name,'w')
    for line in job:
        data_file.write(line)
    data_file.close
    index = index+1

# Debugging                                                                                                                                                                               
#print batched_data                                                                                                                                                                       
#for line in data:                                                                                                                                                                        
#print ">>>"+line                                                                                                                                                                         

# Loop through each job, create a script to submit, and                                                                                                                                   
# submit with qsub                                                                                                                                                                        
for job in range(0,NUMBER_OF_JOBS):
    # Create a job-submission script file                                                                                                                                                 
    job_submit_script_name = "job-submit.%d.sh" % job
    job_submit_script = open(job_submit_script_name,'w')
    job_submit_script.write("#!/bin/sh\n")
    job_submit_script.write("#Job created on: %s\n" % datetime.datetime.utcnow())
    job_submit_script.write("echo 'Job Started: '`date`\n")
    job_submit_script.write("echo 'Running On: '`hostname`\n")
    job_submit_script.write("echo 'Current Working Directory: '`pwd`\n")
    job_submit_script.write("/usr/bin/python myApplication.py --database data.%d.txt --query thequerystringorfile --outfile results.%d.txt --jobid %d" % (job,job,job))
    #job_submit_script.write("sleep %d\n" % job)                                                                                                                                          
    #job_submit_outfile = "out.%d.txt" % job                                                                                                                                              
    #job_submit_script.write("echo 'Job ran on `hostname` and generated this file' > " + job_submit_outfile + "\n")                                                                       
    job_submit_script.close()

    # Submit the script using qsub                                                                                                                                                        
    command = "%s job-submit.%d.sh" % (QSUB_COMMAND,job)
    print "Submitting: " + command
    submitted_job_id = os.system(command)
    print "Job was submitted: %d" % submitted_job_id