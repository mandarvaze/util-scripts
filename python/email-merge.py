#!/usr/bin/env python
#
#       email-merge.py
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
  Initial Structure (including the license lines) created by Geany- A fast and Lightweight IDE  (http://www.geany.org/)

   Following Program can be used to send the same email (with attachment) to several users
   The Code will read the names and email addresses from a CSV file.
   Format of the CSV file should have following columns (without the headers)
   Name,EmailID
'''

import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import csv

'''
 To use this program successfully, you need to change the following set of variables to match your setup and requirements.
 The email addresses, files or the SMTP host IP will not work in your setup
 It is provided here only as reference
'''
EmailMessage = '''
This is a test message

Sent By,
-Email Merge Python Program
'''

sender = "sender@domain.com"
attachments = ["/path/to/file1.jpg","/path/to/file2.txt"] #Files to be attached
smtpserver = "192.168.0.110" #IP Address or hostname is OK
csvfilename = 'data.csv'

nameList = []
mailinglist = []

# Following function taken from http://snippets.dzone.com/posts/show/2038

def send_mail(send_from, send_to, subject, text, files=[], server="localhost"):
  assert type(send_to)==list
  assert type(files)==list

  msg = MIMEMultipart()
  msg['From'] = send_from
  msg['To'] = COMMASPACE.join(send_to)
  msg['Date'] = formatdate(localtime=True)
  msg['Subject'] = subject

  msg.attach( MIMEText(text) )

  for f in files:
    part = MIMEBase('application', "octet-stream")
    part.set_payload( open(f,"rb").read() )
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
    msg.attach(part)

  smtp = smtplib.SMTP(server)
  smtp.sendmail(send_from, send_to, msg.as_string())
  smtp.close()


def parseCSVfile():
    f = open(csvfilename)
    reader = csv.reader(f)
    headerList = reader.next()

    for line in reader:
        # Skip blank lines
        if line:
            if line[1]: #if emailID is available
                nameList.append(line[0])
                mailinglist.append(line[1])
            else:
                print "Email ID missing. Email will not be sent to : '%s'" % line[0]
    f.close()

def extractFirstName(fullName):
    tokens = fullName.split()
    cnt = len(tokens)

#   If First Name is less than one or two character long, it is probably initials
#   In this case, we address the person using the last name
    if len(tokens[0]) <= 2:
        address_as = tokens[cnt-1]
    else:
        address_as = tokens[0]

    return address_as

def main():

    parseCSVfile()

    for index in range(len(mailinglist)):
        emailID = [] # Must be a list as mandated by smtplib
        emailID.append(mailinglist[index])
        address_as_name = extractFirstName(nameList[index])
        print "Sending email to : %s" % nameList[index]
        print ".... Addressed as : %s" % address_as_name
        print ".... At the email address : %s" % mailinglist[index]
        send_mail(sender, emailID, "Put Subject Line Here", ("Dear %s" % address_as_name) + EmailMessage , attachments, smtpserver)

    return 0

if __name__ == '__main__': main()
