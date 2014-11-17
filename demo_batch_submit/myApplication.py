#!/usr/bin/python
import os
import time
import urllib2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--database')
parser.add_argument('--query')
parser.add_argument('--outfile')
parser.add_argument('--jobid')
args = parser.parse_args()

# Fake work that sleeps for the length of the job id (for variation)
time.sleep(int(args.jobid))

# Print the results to a file
results = open(args.outfile,'w')
# Log information out so we know where the job was run
results.write("#### This application would be run with parameters:\n")
results.write("\t> database: " + args.database + "\n")
results.write("\t> query: " + args.query + "\n")
results.write("\t> job id: " + args.jobid + "\n\n")
results.write("#### The results will be written to:\n")
results.write("\t> outfile: " + args.outfile + "\n\n")

# Open the database and dump it to make sure we can see the shared filesystem
results.write("#### The following is the data in " + args.database + ":\n")
db = open(args.database)
results.write(db.read())
db.close()

# Print final statement to check for completion
results.write("#### Job id %s was completed on %s" % (args.jobid,os.uname()[1]))
results.close()