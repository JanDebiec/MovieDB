#!/bin/sh
# a script to start movieDB

cd /home/jan/project/movie_db/
. /home/jan/project/movie_db/venv/bin/activate
#echo $FLASK_APP
flask run

