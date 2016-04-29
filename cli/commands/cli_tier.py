#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import click


class CliTier:
    def __init__(self):
        pass

    def list(self):
        click.echo("tier list")

    def show(self, tiername):
        click.echo("tier show %s" % tiername)

    def run(self, tiername):
        click.echo("tier run %s" % tiername)
