#!/usr/bin/python
import sys
import logging
import os
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/danielgarnacho/tfg/sources/")

from main import app as application
application.secret_key = '\xa8T\x089\x81#\xd1\x02/\xdb\x8d\xe0\x13\x8e-\x97\xe0k\x93\x96h\xfci\x1c'
