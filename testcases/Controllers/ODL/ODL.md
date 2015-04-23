# Robotframework test for ODL

Original ODL testsuites can be found here: https://github.com/opendaylight/integration

## Environment for running tests

Create python virtual environment and install following packages into it:

BeautifulSoup==3.2.1
PyYAML==3.11
contextdecorator==0.10.0
ecdsa==0.11
ipaddr==2.1.11
paramiko==1.14.0
pycrypto==2.6.1
pystache==0.5.4
requests==2.3.0
robotframework==2.8.5
robotframework-requests==0.3.7
robotframework-sshlibrary==2.0.2
six==1.7.3
vcrpy==1.0.2
wsgiref==0.1.2

## Running tests
For more info:
cd CI
bash start_test.sh -h
