#!/usr/bin/env python2
#!/usr/bin/env python2
import sys
from asterisk.agi import *
from gtts import gTTS
from pycall import CallFile, Call, Application
import os
import time
import commands
import MySQLdb
import re
def playInboundAnnc(inboundAnncText):
 agi.verbose("am in function1")
 tts = gTTS(text=inboundAnncText, lang='en')
 tts.save("inboundAnnc.mp3")
 os.system("mpg321 inboundAnnc.mp3")
 agi.verbose("am in function2")
 os.system("sudo sox inboundAnnc.mp3 -r 8000 -c1 inboundAnnc.gsm")
 os.system("cp inboundAnnc.gsm /var/lib/asterisk/sounds/en/")
 agi.verbose("am in function3")
 agi.stream_file('inboundAnnc')


agi = AGI()
agi.verbose("python agi started")
db = MySQLdb.connect (host = "localhost", user = "test", passwd = "test123", db = "tkr")
cursor = db.cursor()

callerId = agi.env['agi_callerid']
agi.verbose("call from %s" % callerId)


#playInboundAnnc(inboundAnncText)
agi.stream_file('welcome')
#agi.stream_file('hello-world')

def play():
    agi.stream_file('welcome')


 

while True:
  result = agi.wait_for_digit(-1)
  agi.verbose("got digit %s" % result)
  sqlcommand="select name from studentdet  where rollno='"+callerId+"'"
  agi.verbose(sqlcommand)
  cursor.execute(sqlcommand)
  row = cursor.fetchall()
  studentName = str(row[0][0])
  
  if result=="1":
    sqlcommand="select a.rollno,a.name,b.subname,b.marks from studentdet a, marks b where a.rollno=b.rollno and a.rollno='"+callerId+"'"
    agi.verbose(sqlcommand)
    cursor.execute(sqlcommand)
    agi.verbose('test1')
    row = cursor.fetchall()
   
    inboundAnncText='Dear '+studentName+ ' you got ' +str(row[0][3])+' in  '+str(row[0][2])+' subject Thank you '
    agi.verbose('test3')
    agi.send_text(text=inboundAnncText)
    # agi.send_text(text='inboundAnncText')
    agi.verbose(inboundAnncText)
    playInboundAnnc(inboundAnncText)
    play()
    
  if result=="2":
    
    sqlcommand="select a.rollno,a.name,c.percentage from studentdet a,attendance c where a.rollno=c.rollno and a.rollno='"+callerId+"'"
    
    agi.verbose(sqlcommand)
    cursor.execute(sqlcommand)
    row = cursor.fetchall()
    inboundAnncText='Dear '+studentName+ '  your attendance percentage is  ' +str(row[0][2])+'  Thank you '
    agi.verbose(inboundAnncText)
    agi.send_text(text=inboundAnncText)

    playInboundAnnc(inboundAnncText)
    play()
    
  if result=="3":
    sqlcommand="select a.rollno,a.name,d.period1,d.period2,d.period3 from studentdet a, schedule d where d.year =substr('"+callerId+"',1,2) and d.branch =substr('"+callerId+"',8,1)"
    agi.verbose(sqlcommand)
    cursor.execute(sqlcommand)
    row = cursor.fetchall()
    inboundAnncText='Dear  '+studentName+' your schedule for first period is '+str(row[0][2])+' second period is '+str(row[0][3])+' third period is  '+str(row[0][4])+' Thank you'
    agi.verbose(inboundAnncText)
    agi.send_text(text=inboundAnncText)
    playInboundAnnc(inboundAnncText)
    play()
    
  if result=="4":
    play()
 
  else :
   agi.verbose("bye!")
   agi.hangup()
   sys.exit()
