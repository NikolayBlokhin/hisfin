#!/usr/bin/env python3
# -*- coding: utf-8 -*-


API_URL = "https://api-demo.exante.eu/md/1.0"
TOKEN_EXPIRATION = 3600   # in seconds


API_CLIENT_ID = ''
API_APP_ID = ''
API_SHARED_KEY = ''


try:
    from local_settings import *
except ImportError:
    print('WARNING: There is no "local_settings.py"!')
