#!/bin/bash

gunicorn --chdir app main:app -w 4 --threads 2 -b 0.0.0.0:5000