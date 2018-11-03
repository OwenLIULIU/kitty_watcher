#!/bin/bash

# create and enter virtualenv
if [ ! -d "env" ]; then
  virtualenv env
fi
. env/bin/activate

# install flake8
pip install flake8
pip install flake8-import-order

# install requirements
pip install -r requirements.txt
pip install -e .
