#!/usr/bin/env bash
# a script to start movieDB

cd /home/ubuntu/project/MovieDb/
. /home/ubuntu/project/MovieDb/venv/bin/activate
echo $FLASK_APP
flask run

