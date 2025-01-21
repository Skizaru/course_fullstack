# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# bind = '0.0.0.0:5005'
# workers = 1
# accesslog = '-'
# loglevel = 'debug'
# capture_output = True
# enable_stdio_inheritance = True


workers = 1
worker_class = "gevent"
bind = "0.0.0.0:5005"
timeout = 60
loglevel = "debug"
errorlog = "-"
accesslog = "-"
capture_output = True
enable_stdio_inheritance = True