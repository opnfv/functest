#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import click


class CliTestcase:
    def __init__(self):
        pass

    def list(self):
        click.echo("testcase list")

    def show(self, testname):
        click.echo("testcase show %s" % testname)

    def run(self, testname):
        click.echo("testcase run %s" % testname)
