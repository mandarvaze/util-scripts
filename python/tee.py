'''
---------- License Details ----------
The source code is licensed under "The MIT License"
http://www.opensource.org/licenses/mit-license.php

Read the License.txt for details.
--------------------------------------

This is implementation of unix utility named "tee" in python
It is helpful when you need to run some command that generates
lots of output on the console
This utility allows the users to see the output on the console
as they would normally, but in addition is also captures the same
output in a logfile, for later perusal

Change the values of global variables 'cmd' and 'workdir' below.
Later these will be entered by the user as command line parameters
Run this tool as "python tee.py"

Mandar Vaze (mandarvaze@gmail.com)

'''
import subprocess
import sys
from time import strftime
#from optparse import OptionParser

timestamp = strftime("%Y-%m-%d-%H-%M-%S")
#TODO : Make these are command line parameters using OprionParser
logfilename = "tee-%s.log" % timestamp
cmd = "dir *.* /s/B"
workdir = "C:\\WINDOWS\system32"

def tee():
	file = open(logfilename,"w")
	proc = subprocess.Popen(cmd,cwd=workdir,shell=True,stdout=subprocess.PIPE)
	while 1:
		out = proc.stdout.readline()
		if (len(out) == 0):
			break
		file.write(out)
		print out

	proc.communicate()
	file.close

def main():
#TODO: Use OptionPraser to get the inputs from user, rather than modifying the scripts each time.
	tee()

if __name__ == "__main__":
	if (sys.platform == "win32"):
	   cmd = "dir *.* /s/B"
	   workdir = "C:\\WINDOWS\system32"
	else: #May be Unix platform. What are good default for OS X ?
	   cmd = "ls -l"
	   workdir = "/tmp"

	sys.exit(main())

