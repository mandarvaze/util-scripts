#!/usr/bin/env python
#
#       tee.py
#
#       Copyright 2009 Mandar Vaze (mandarvaze@gmail.com)
#
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''
This is implementation of unix utility named "tee" in python
It is helpful when you need to run some command that generates
lots of output on the console
This utility allows the users to see the output on the console
as they would normally, but in addition is also captures the same
output in a logfile, for later perusal

Change the values of global variables 'cmd' and 'workdir' below.
Later these will be entered by the user as command line parameters
Run this tool as "python tee.py"

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

