#!/usr/bin/env bash

cd /home/ubuntu/project
sudo rsync -rv --exclude 'venv/' --exclude 'imdbif/' MovieDB/ admin@192.168.178.197:/volume1/MovieDB/