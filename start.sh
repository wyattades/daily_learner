#!/bin/bash

PASSWORD=1234

cd ../..
python web2py.py -a "$PASSWORD" -p 3000
