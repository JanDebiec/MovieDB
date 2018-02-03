#!/usr/bin/env bash
# a script to start movieDB

cd /home/ubuntu/project/MovieDB/
. /home/ubuntu/project/MovieDB/venv/bin/activate
echo $FLASK_APP
flask run

