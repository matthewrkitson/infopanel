#!/bin/bash

cd $(dirname $0)
git fetch origin
git checkout origin/master
source venv/bin/activate
pip install -r requirements.txt
python3 infopanel.py

