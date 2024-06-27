#!/usr/bin/env python2
import sys
from pycall import CallFile, Call, Application
from gtts import gTTS
import os
import time
import commands
import MySQLdb
status, output = commands.getstatusoutput('sudo asterisk -rnx "sip show peers"')
#print(status,"output=",output,"end")
#time.sleep(2)
print("hello")


db = MySQLdb.connect (host = "localhost", user = "root", passwd = "rttc123", db = "tkr")
cursor = db.cursor()
sqlcommand="update profile set status='unknown' where status = 'REGISTERED'"
cursor.execute(sqlcommand)
db.commit()

#myfile=open("user")
#filedata=myfile.readlines()

filedata=output.split("\n")
for line in filedata:
 words=line.split()
 if(words[1]!="(Unspecified)" and words[1]!="sip" and words[1]!="Host"):
  #print(words[0].replace(" ",""),",",words[1].replace(" ",""))
  print(words[0].split("/")[0])
  reguser=words[0].split("/")[0]
  #call = Call('SIP/'+words[0].split("/")[0])
  #action = Application('Playback', 'rams')
  #c = CallFile(call, action)
  #c.spool()
  
  sqlcommand="update profile set time = now() ,status='REGISTERED' where rollno = '"+reguser+"'"
  print(sqlcommand)
  cursor.execute(sqlcommand)
  db.commit()

print('registation of attendance of faculty')
cursor.execute('select * from profile where length(rollno) != 10')
facdata = cursor.fetchall()
for row in facdata:
    print(row[1],row[3],row[4])
print('registation of attendance of students')
cursor.execute('select * from profile where length(rollno) = 10')
facdata = cursor.fetchall()
for row in facdata:
    print(row[1],row[3],row[4])
 
sqlcommand="select substr(rollno,1,2) year,substr(rollno,8,1) grp ,status,count(1) noofstudents  from profile where  status='REGISTERED'  group by substr(rollno,1,2),substr(rollno,8,1),status"
 
print('registation of attendance of students')
cursor.execute(sqlcommand)
facdata = cursor.fetchall()
for row in facdata:
    print(row[0],row[1],row[2],row[3])
 
        
