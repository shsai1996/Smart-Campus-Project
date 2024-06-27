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

agi = AGI()
agi.verbose("python agi started")
agi.verbose(agi.env['agi_arg_1'])
#agi.send_text(text=agi_arg_1)
agi.stream_file('rams')
agi.verbose("python agi started2")
agi.verbose("python agi started3")
agi.send_text(text=" test sms ")
agi.send_text(text=agi.env['agi_arg_1'])
agi.send_text(text=inboundAnncText)


    
