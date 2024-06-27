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
 tts = gTTS(text=inboundAnncText, lang='en')
 tts.save("inboundAnnc.mp3")
 os.system("mpg321 inboundAnnc.mp3")
 os.system("sudo sox inboundAnnc.mp3 -r 8000 -c1 welcome.gsm")
 os.system("cp welcome.gsm /var/lib/asterisk/sounds/en/")
playInboundAnnc("Welcome to TKR Announcemnet system press 1 marks press 2 for  attendance press 3 todays schedule Thank you")  
