#!/bin/bash

set -e
cd $(dirname $0)

if [ ! -d ../common ] ; then
	echo "assumed to be in submodule structure"
	exit 1
fi

ln -s ../common/*.py .
ln -s ../faqbot/join_channels.py

if [ ! -e Main.conf ]; then
	cp Main.conf.example Main.conf
fi
