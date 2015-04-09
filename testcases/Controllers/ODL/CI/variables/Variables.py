"""
Library for the robot based system test tool of the OpenDaylight project.
"""
import collections

# Global variables
CONTROLLER = '10.2.91.18'
PORT = '8081'
PREFIX = 'http://' + CONTROLLER + ':' + PORT
USER = 'admin'
PWD = 'admin'
AUTH = [u'admin',u'admin']
HEADERS={'Content-Type': 'application/json'}
HEADERS_XML={'Content-Type': 'application/xml'}
ACCEPT_XML={'Accept': 'application/xml'}

#TOKEN
AUTH_TOKEN_API='/oauth2/token'
REVOKE_TOKEN_API='/oauth2/revoke'

