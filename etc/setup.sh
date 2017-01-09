#!/bin/sh
# -*- coding: utf-8 -*-

virtualenv --no-site-packages -p python3 env

source ./env/bin/activate

pip install -r ./etc/requirements.txt






