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
# 0.1: This script creates the needed local files into a tmp directory. Should
# '--clean' be passed, all files will be removed, post scan.


import os
import tempfile

files = ['results.xml', 'report.html', 'syschar.xml']


directory_name = tempfile.mkdtemp()

for i in files:
    os.system("touch %s/%s" % (directory_name, i))

print directory_name
