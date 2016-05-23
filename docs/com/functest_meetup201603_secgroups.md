OPNFV Meetup 2016.03.30
==============================

**Subject**: New tests bundle: security groups

**Author**: David Blaisonneau - Orange

Goal
------------------

Today no test in OPNFV is focused on security group testing.

Security groups is a key element for VNF

We know by experience that security groups is not well handle by some scenarios. Moreover, security groups can be set
but are not functionals, giving the illusion of security.

Today, security groups can be handle by Openstack Neutron L3 or delegated to the SDN controller.

=> Propostion to add security group tests bundle in functest


Tests list proposition
----------------------

**API testing**:

- Create/ModifyDelete Security Group (SG)
- Add/Modify/Delete Security Rules (SR) to SG
    - with different parameters: protocol, source address, destination port, ingress/egress, IPv4/IPv6
- Apply/remove a SG to a VNF

**SG testing**:

(for each test, no SG are set before, and all are removed after)

- Protocol testing:
    - ICMP:
        - test ping fails
        - add an ICMP SG/SR
        - test ping success
        - remove SR
        - test ping fails
    - TCP: 
        - tcp connection to port 22 fails
        - add an SSH SG/SR
        - tcp connection success
        - remove SR
        - tcp connection fails
    - UDP: 
        - udp connection to port 53 fails
        - add an DNS SG/SR
        - udp connection success
        - remove SR
        - udp connection fails
- Source/Destination testing (TCP case):
    - authorize a TCP (SSH) connection from one source and not the other:
        - set SG/SR with SSH connection authorized from VNF network (Ingress rule)
        - SSH is rejected for public network
        - SSH is accepted from another VNF in the same network
    - authorize TCP (HTTP) connection to a destination and not the other
        - set SG/SR with all connections authorized to VNF network (Egress rule)
        - HTTP request is rejected to public network
        - HTTP request is rejected to another VNF in the same network


Testing infrastructure
----------------------

- Based on vPing test case.
- Tests done from the functest container, directly or using a ssh connection (for VNF to VNF tests)
- 2 VNF on the same tenant, the same network and one with a floating ip.
    
       Openstack API    Internet HTTP server
           ^                    ^                                                                
           |                    |                                                                
    +--------------+            |        +--------------+   +-------------+
    | functest     |            |        |  VM 1        |   | VM 2        |
    | container    |            |        |  ICMP        |   | ICMP        |
    |              |    FIP 1   |        |  TCP 22 / 80 |   | TCP 22 / 80 |
    |              |----> Tenant Router  |  ICMP 53     |   |             |
    |              |            |        |              |   |             |
    +--------------+            |        +--------------+   +-------------+
                                |                 ^ IP 1          ^ IP 2
                                |                 |               |    
                                +-----------------+---------------+    

- Test in python using openstack api and tcp/icmp/udp connection libs.

**Test pre requisits**: vPing **<span style='color:#00FF00'>OK</span>**


Comments ?
--------------
