#!/bin/sh

cd /home/pi/fmapi
gunicorn  --reload -c gunicorn.conf index:app;
