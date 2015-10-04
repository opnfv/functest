"""
Description:
    This file include basis functions
    lanqinglong@huawei.com
"""

import logging
import os
import time

class foundation:

    def __init__(self):
        self.dir = os.path.join( os.getcwd(), 'log' )

    def log (self, loginfo):
        """
        Record log in log directory for deploying test environment
        parameters:
        loginfo(input): record info
        """
        filename = time.strftime( '%Y-%m-%d-%H-%M-%S' ) + '.log'
        filepath = os.path.join( self.dir, filename )
        logging.basicConfig( level=logging.INFO,
                format = '%(asctime)s %(filename)s:%(message)s',
                datefmt = '%d %b %Y %H:%M:%S',
                filename = filepath,
                filemode = 'w')
        filelog = logging.FileHandler( filepath )
        logging.getLogger( 'Functest' ).addHandler( filelog )
        print loginfo
        logging.info(loginfo)