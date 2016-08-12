#!/usr/bin/python
#
# Copyright (c) 2016 Red Hat
# Luke Hinds (lhinds@redhat.com)
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Performs simple connection check, falls to default timeout of 10 seconds

import socket
TEST_HOST = "google.com"
def is_connected():
  try:
    host = socket.gethostbyname(TEST_HOST)
    sock = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
     return False
print is_connected()
