##############################################################################
# Copyright (c) 2015 EMC and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from setuptools import setup, find_packages


setup(
    name="functest",
    version="colorado.2.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
    },
    url="https://www.opnfv.org",
    install_requires=["click==6.6"],
    entry_points={
    }
)

