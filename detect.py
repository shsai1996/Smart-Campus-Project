#!/usr/bin/env python2
#!/usr/bin/env python2
import os, time
from time import gmtime, strftime
import sys
from pycall import CallFile, Call, Application
from gtts import gTTS
import os
import time
import commands
import MySQLdb
def playAnnc(anncText):
 tts = gTTS(text=anncText, lang='en')
 tts.save("anncText.mp3")
 os.system("sudo sox anncText.mp3 -r 8000 -c1 anncText.gsm")
 os.system("cp anncText.gsm /var/lib/asterisk/sounds/en/")


db = MySQLdb.connect (host = "localhost", user = "root", passwd = "rttc123", db = "tkr")
cursor = db.cursor()

(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat("/var/log/asterisk/smart")
prevmod=time.ctime(mtime)
print(" Waiting for new registrations")
while True:
 while(prevmod==time.ctime(mtime)):
  (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat("/var/log/asterisk/smart")
  #print("last modified: %s" % time.ctime(mtime))
  time.sleep(1)
 prevmod=time.ctime(mtime)
 with open("/var/log/asterisk/smart") as fd:
  data=fd.read()
  #print(data)
  regIndex=data.rfind("Registered SIP")+len("Registered SIP")+2
  #temp=data[regIndex:]
  regendIndex=data.rfind('at')-2
  #print(regIndex)
  #unregIndex=data.rfind("Unregistered SIP ")+len("Unregistered SIP ")+2
  veroseLoc=data.rfind("VERBOSE")+len("VERBOSE")+2
  if(regIndex > veroseLoc):
   regUser=(data[regIndex:regendIndex])
   #print(regUser,regIndex,regendIndex)
   
   sqlcommand="update profile set time = now() ,status='REGISTERED' where rollno = '"+regUser+"'"
   print(sqlcommand)
   cursor.execute(sqlcommand)
   db.commit()
   
   print("Calling to new registered user:"+regUser)
   #sqlCommand = "SELECT * FROM schedule where rollno='"+regUser+"'"
   sqlCommand = "SELECT * FROM schedule where year= substr('"+regUser+"',1,2) and branch = substr('"+regUser+"',8,1)"
   print(sqlCommand)
   cursor.execute(sqlCommand)
   row = cursor.fetchall()
   anncText="Hello "+regUser+" Taking your picture stand infront of webcam for 20 seconds Today You have First class "+row[0][2]+" and Second class "+row[0][3]+" Third class "+row[0][4]+" Fourth class "+row[0][5]+" Fifth class "+row[0][6]+" Sixth class "+row[0][7]+" Thank you have a nice day"
   print(anncText)
   playAnnc(anncText)
   time.sleep(1)
   call = Call('SIP/'+regUser)
   action = Application('Playback', 'anncText')
   c = CallFile(call, action)
   c.spool()
   time.sleep(5)
   camCommand="fswebcam -r 1280x720 -S 20 "+regUser+strftime("%H%M%S", gmtime())
   sqlcommand="update profile set picture = '"+camCommand+"' where rollno = '"+regUser+"'"
   print(sqlcommand)
   cursor.execute(sqlcommand)
   db.commit()
   print("Taking picture:"+regUser)
   os.system(camCommand)
 
