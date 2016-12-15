##############################################################################
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from setuptools import setup, find_packages


setup(
    name="functest",
    version="master",
    py_modules=['cli_base'],
    packages=find_packages(),
    include_package_data=True,
    package_data={
    },
    url="https://www.opnfv.org",
    entry_points={
        'console_scripts': [
            'functest=functest.cli.cli_base:cli'
        ],
    },
)
