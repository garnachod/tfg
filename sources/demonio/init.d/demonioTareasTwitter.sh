#!/bin/bash

# Copyright (c) 1996-2012 My Company.

# All rights reserved.

#

# Author: Daniel Garnacho, edit from http://blog.crespo.org.ve/2014/02/crear-un-demonio-de-linux-con-python.html

#

# Please send feedback to garnachod@gmail.com

#

# /etc/init.d/demonioTareasTwitter

#

### BEGIN INIT INFO

# Provides: demonioTareasTwitter

# Required-Start: $all

# Should-Start: $all

# Required-Stop:

# Should-Stop:

# Default-Start:  2 3 4 5

# Default-Stop:   0 1 6

# Short-Description: Test daemon process

# Description:    Runs up the test daemon process

### END INIT INFO



# Activate the python virtual environment

#    . /path_to_virtualenv/activate

############### EDIT ME ##################
# path to app
APP_PATH=/home/dani/tfg/tfg/sources/demonioTareasTwitter.py


############### END EDIT ME ##################


case "$1" in
  start)
    echo "Starting server"
    # Start the daemon
    python $APP_PATH start
    ;;
  stop)
    echo "Stopping server"
    # Stop the daemon
    python $APP_PATH stop
    ;;
  restart)
    echo "Restarting server"
    python $APP_PATH restart
    ;;
  *)
    # Refuse to do other stuff
    echo "Usage: /etc/init.d/demonioTareasTwitter.sh {start|stop|restart}"
    exit 1
    ;;
esac
exit 0

