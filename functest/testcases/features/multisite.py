#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Execute Multisite Tempest test cases
#
import functest.utils.functest_logger as ft_logger

logger = ft_logger.Logger("multisite").getLogger()


def main():
    logger.info("multisite OK")

if __name__ == '__main__':
    main()
