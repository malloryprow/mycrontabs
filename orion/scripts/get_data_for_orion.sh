#!/bin/sh
[ -f /etc/bashrc ] && . /etc/bashrc

# Load modules
module load python/3.10.8

# Set environment variables
export CP=`which cp | sed 's/cp is //g'`
export WGET=`which wget | sed 's/wget is //g'`
export RSYNC=`which rsync | sed 's/rsync is //g'`

python /home/mrow/mycronjobs/scripts/get_data_for_orion.py
