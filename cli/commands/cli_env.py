#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import click


class CliEnv:
    def __init__(self):
        pass

    def show(self):
        click.echo("env show")

    def status(self):
        click.echo("env status")

    def getrc(self):
        click.echo("env getrc")

    def sourcerc(self):
        click.echo("env sourcerc")

    def setdefaults(self):
        click.echo("env setdefaults")

    def getdefaults(self):
        click.echo("env getdefaults")

    def clean(self):
        click.echo("env clean")
