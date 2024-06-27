#!/usr/bin/env python2
from asterisk.agi import *
import sys
from pycall import CallFile, Call, Application
from gtts import gTTS
import os
import time
import commands
status, output = commands.getstatusoutput('sudo asterisk -rnx "sip show peers"')
print(status,"output=",output,"end")
time.sleep(2)
print("hello ")
#myfile=open("user")
#filedata=myfile.readlines()
tellmsg=sys.argv[1]
tts = gTTS(text= sys.argv[1], lang='en')

tts.save("rams.mp3")
print("hello ")
#os.system("mpg321 rams.mp3")
os.system("sudo sox rams.mp3 -r 8000 -c1 rams.gsm")
os.system("cp rams.gsm /var/lib/asterisk/sounds/en/")
filedata=output.split("\n")
print(tellmsg)
for line in filedata:
 words=line.split()
 if(words[1]!="(Unspecified)" and words[1]!="sip" and words[1]!="Host"):
  #print(words[0].replace(" ",""),",",words[1].replace(" ",""))
  print(words[0].split("/")[0])
  user=words[0].split("/")[0]
  if(sys.argv[2] == '1')and(len(user) == 10):
   call = Call('SIP/'+words[0].split("/")[0])
   action = Application('Playback', 'rams')
   c = CallFile(call, action)
   c.spool()
  if(sys.argv[2] == '2')and(len(user) == 3):
   call = Call('SIP/'+words[0].split("/")[0])
   action = Application('Playback', 'rams')
   c = CallFile(call, action)
   c.spool() 
  if(sys.argv[2] == '3'):
   call = Call('SIP/'+words[0].split("/")[0])
   cmdData=  "ob.py,"+tellmsg
   print(cmdData)
   action = Application('agi',cmdData)
   #agi.send_text(text=rams)
   c = CallFile(call, action)
   c.spool()       
   #agi.send_text(text=tellmsg)
