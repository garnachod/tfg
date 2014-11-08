#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/danielgarnacho/tfg/")

from sources import app as application
application.secret_key = os.urandom(24)
