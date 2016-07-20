"""SFC functions."""
import json
from multiprocessing import Process
from multiprocessing import Queue
import os
import re
import time

import functest.utils.functest_logger as ft_logger
from pexpect import pxssh
import requests


class Sfc_fun:
    """Defines all the def function of SFC."""

    def __init__(self):
        """Initialization of variables."""
        self.logger = ft_logger.Logger("sfc_fun").getLogger()
        self.osver = "v2.0"
        self.token_id = 0
        self.net_id = 0
        self.image_id = 0
        self.keystone_hostname = 'keystone_ip'
        self.neutron_hostname = 'neutron_ip'
        self.nova_hostname = 'nova_ip'
        self.glance_hostname = 'glance_ip'
        self.onos_hostname = 'onos_ip'
        # Network variables #######
        self.netname = "test_nw"
        self.admin_state_up = True
        self.tenant_id = 0
        self.subnetId = 0
        # #########################
        # SubNet variables#########
        self.ip_version = 4
        self.cidr = "20.20.20.0/24"
        self.subnetname = "test_nw_subnets"
        # ###############################
        # Port variable
        self.port = "port"
        self.port_num = []
        self.vm_id = 0
        self.port_ip = []
        self.count = 0
        self.i = 0
        self.numTerms = 3
        self.security_groups = []
        self.port_security_enabled = False
        # ###############################
        # VM creation variable
        self.container_format = "bare"
        self.disk_format = "qcow2"
        self.imagename = "TestSfcVm"
        self.createImage = "/home/root1/devstack/files/images/\
                            firewall_block_image.img"

        self.vm_name = "vm"
        self.imageRef = "test"
        self.flavorRef = "1"
        self.max_count = "1"
        self.min_count = "1"
        self.org_nw_port = []
        self.image_id = 0
        self.routername = "router1"
        self.router_id = 0
        # #####################################
        # Port pair
        self.port_pair_ingress = 0
        self.port_pair_egress = 0
        self.port_pair_name = "PP"
        self.port_pair_id = []
        # ####################################
        # Port Group
        self.port_group_name = "PG"
        self.port_grp_id = []
        # ####################################
        # FlowClassifier
        self.source_ip_prefix = "20.20.20.0/24"
        self.destination_ip_prefix = "20.20.20.0/24"
        self.logical_source_port = 0
        self.fcname = "FC"
        self.ethertype = "IPv4"
        # #####################################
        self.flow_class_if = 0
        # #####################################
        # Port Chain variables
        self.pcname = 'PC'
        self.PC_id = 0
        # #####################################
        # Port Chain variables
        self.flowadd = ''
        # #####################################
        self.ip_pool = 0
        self.vm_public_ip = []
        self.vm_public_id = []
        self.net_id1 = 0
        self.vm = []
        self.address = 0
        self.value = 0
        self.pub_net_id = 0

    def getToken(self):
        """Get the keystone token value from Openstack ."""
        url = 'http://' + self.keystone_hostname + \
            ':5000/' + self.osver + '/tokens'
        data = '{"auth": {"tenantName": "admin",  "passwordCredentials":\
                { "username": "admin", "password": "console"}}}'
        headers = {"Accept": "application/json"}
        response = requests.post(url, headers=headers,  data=data)
        if (response.status_code == 200):
            json1_data = json.loads(response.content)
            self.logger.debug(response.status_code)
            self.logger.debug(response.content)
            self.logger.debug(json1_data)
            self.token_id = json1_data['access']['token']['id']
            self.tenant_id = json1_data['access']['token']['tenant']['id']
            return(response.status_code)
        else:
            return(response.status_code)

    def createNetworks(self):
        """Creation of networks."""
        Dicdata = {}
        if self.netname != '':
            Dicdata['name'] = self.netname
        if self.admin_state_up != '':
            Dicdata['admin_state_up'] = self.admin_state_up
        Dicdata = {'network': Dicdata}
        data = json.dumps(Dicdata,  indent=4)
        url = 'http://' + self.neutron_hostname + \
            ':9696/' + self.osver + '/networks'
        headers = {"Accept": "application/json",
                   "X-Auth-Token": self.token_id}
        response = requests.post(url, headers=headers,  data=data)
        if (response.status_code == 201):
            self.logger.debug(response.status_code)
            self.logger.debug(response.content)

            json1_data = json.loads(response.content)
            self.logger.debug(json1_data)
            self.net_id = json1_data['network']['id']
            return(response.status_code)
        else:
            return(response.status_code)

    def createSubnets(self):
        """Creation of SubNets."""
        Dicdata = {}
        if self.net_id != 0:
            Dicdata['network_id'] = self.net_id
        if self.ip_version != '':
            Dicdata['ip_version'] = self.ip_version
        if self.cidr != '':
            Dicdata['cidr'] = self.cidr
        if self.subnetname != '':
            Dicdata['name'] = self.subnetname

        Dicdata = {'subnet': Dicdata}
        data = json.dumps(Dicdata, indent=4)
        url = 'http://' + self.neutron_hostname + \
            ':9696/' + self.osver + '/subnets'
        headers = {"Accept": "application/json",
                   "X-Auth-Token": self.token_id}
        response = requests.post(url, headers=headers,  data=data)

        if (response.status_code == 201):
            self.logger.debug(response.status_code)
            self.logger.debug(response.content)
            json1_data = json.loads(response.content)
            self.logger.debug(json1_data)
            self.subnetId = json1_data['subnet']['id']
            return(response.status_code)
        else:
            return(response.status_code)

    def createPorts(self):
        """Creation of Ports."""
        for x in range(self.i, self.numTerms):
            Dicdata = {}
            if self.net_id != '':
                Dicdata['network_id'] = self.net_id
            if self.port != '':
                Dicdata['name'] = "port" + str(x)
            if self.admin_state_up != '':
                Dicdata['admin_state_up'] = self.admin_state_up
            if self.security_groups != '':
                Dicdata['security_groups'] = self.security_groups
            # if self.port_security_enabled != '':
            #    Dicdata['port_security_enabled'] = self.port_security_enabled

            Dicdata = {'port': Dicdata}
            data = json.dumps(Dicdata, indent=4)
            url = 'http://' + self.neutron_hostname + \
                ':9696/' + self.osver + '/ports'
            headers = {"Accept": "application/json",
                       "X-Auth-Token": self.token_id}
            response = requests.post(url, headers=headers,  data=data)

            if (response.status_code == 201):
                self.logger.debug(response.status_code)
                self.logger.debug(response.content)

                json1_data = json.loads(response.content)
                self.logger.debug(json1_data)
                self.port_num.append(json1_data['port']['id'])
                self.port_ip.append(json1_data['port']['fixed_ips'][0]
                                    ['ip_address'])
            else:
                return(response.status_code)
        return(response.status_code)

    def createVm(self):
        """Creation of Instance, using  firewall image."""
        url = 'http://' + self.glance_hostname + \
            ':9292/v2/images?name=TestSfcVm'
        headers = {"Accept": "application/json", "Content-Type": "application/\
                    octet-stream",  "X-Auth-Token": self.token_id}
        response = requests.get(url, headers=headers)
        if (response.status_code == 200):
            self.logger.debug(response.status_code)
            self.logger.debug(response.content)
            self.logger.info("\tFireWall Image is available")
            json1_data = json.loads(response.content)
            self.logger.debug(json1_data)
            self.image_id = json1_data['images'][0]['id']
        else:
            return(response.status_code)

        for y in range(0, 3):
            Dicdata = {}
            org_nw_port = []
            org_nw_port.append({'port': self.port_num[y]})
            if self.vm_name != '':
                Dicdata['name'] = "vm" + str(y)
            if self.imageRef != '':
                Dicdata['imageRef'] = self.image_id
            if self.flavorRef != '':
                Dicdata['flavorRef'] = self.flavorRef
            if self.max_count != '':
                Dicdata['max_count'] = self.max_count
            if self.min_count != '':
                Dicdata['min_count'] = self.min_count
            if self.org_nw_port != '':
                Dicdata['networks'] = org_nw_port
            Dicdata = {'server': Dicdata}
            data = json.dumps(Dicdata, indent=4)

            url = ('http://' + self.nova_hostname + ':8774/v2.1/' +
                   self.tenant_id + '/servers')
            headers = {"Accept": "application/json", "Content-Type":
                       "application/json", "X-Auth-Token": self.token_id}
            response = requests.post(url, headers=headers,  data=data)
            if (response.status_code == 202):
                self.logger.debug(response.status_code)
                self.logger.debug(response.content)
                self.logger.info("\tCreation of VM is successfull")

                json1_data = json.loads(response.content)
                self.logger.debug(json1_data)
                self.vm_id = json1_data['server']['id']
                self.vm.append(json1_data['server']['id'])
            else:
                return(response.status_code)

        return(response.status_code)

    def checkVmState(self):
        """Checking the Status of the Instance."""
        time.sleep(10)
        for y in range(0, 3):
            url = 'http://' + \
                  self.nova_hostname + \
                ':8774/v2.1/servers/detail?name=vm' + str(y)
            headers = {"Accept": "application/json",  "X-Auth-Token":
                       self.token_id}
            response = requests.get(url, headers=headers)
            if (response.status_code == 200):
                self.logger.debug(response.status_code)
                self.logger.debug(response.content)
                json1_data = json.loads(response.content)
                self.logger.debug(json1_data)
                self.vm_active = json1_data['servers'][0]['status']
                if (self.vm_active == "ACTIVE"):
                    print ("\t\t\t\t\t\tVM" + str(y) + " is Active : " +
                           self.vm_active)
                else:
                    print ("\t\t\t\t\t\tVM" + str(y) + " is NOT Active : " +
                           self.vm_active)
            else:
                return(response.status_code)
        return(response.status_code)
        time.sleep(10)

    def createPortPair(self):
        """Creation of Port Pair."""
        for p in range(1, 2):
            Dicdata = {}
            if self.port_pair_ingress != '':
                Dicdata['ingress'] = self.port_num[p]
            if self.port_pair_egress != '':
                egress = p
                Dicdata['egress'] = self.port_num[egress]
            if self.port_pair_name != '':
                Dicdata['name'] = "PP" + str(p)

            Dicdata = {'port_pair': Dicdata}
            data = json.dumps(Dicdata, indent=4)

            url = 'http://' + self.neutron_hostname + ':9696/' + self.osver + \
                '/sfc/port_pairs'
            headers = {"Accept": "application/json", "X-Auth-Token":
                       self.token_id}
            response = requests.post(url, headers=headers,  data=data)
            if (response.status_code == 201):
                print ("\t\t\t\tCreation of Port Pair PP" + str(p) +
                       " is successful")
            else:
                return(response.status_code)

        return(response.status_code)

    def getPortPair(self):
        """Query the Portpair id value."""
        for p in range(0, 1):
            url = 'http://' + self.neutron_hostname + ':9696/' + self.osver + \
                  '/sfc/port_pairs?name=PP1'
            headers = {"Accept": "application/json", "X-Auth-Token":
                       self.token_id}
            response = requests.get(url, headers=headers)

            if (response.status_code == 200):
                self.logger.debug(response.status_code)
                self.logger.debug(response.content)
                json1_data = json.loads(response.content)
                self.logger.debug(json1_data)
                self.port_pair_id.append(json1_data['port_pairs'][0]['id'])
            else:
                return(response.status_code)
        return(response.status_code)

    def createPortGroup(self):
        """Creation of PortGroup."""
        for p in range(0, 1):
            Dicdata = {}
            port_pair_list = []
            port_pair_list.append(self.port_pair_id[p])
            if self.port_group_name != '':
                Dicdata['name'] = "PG" + str(p)
            if self.port_pair_id != '':
                Dicdata['port_pairs'] = port_pair_list

            Dicdata = {'port_pair_group': Dicdata}
            data = json.dumps(Dicdata, indent=4)
            url = 'http://' + self.neutron_hostname + ':9696/' + self.osver + \
                  '/sfc/port_pair_groups'
            headers = {"Accept": "application/json", "X-Auth-Token":
                       self.token_id}
            response = requests.post(url, headers=headers,  data=data)
            if (response.status_code == 201):
                print ("\t\t\t\tCreation of Port Group PG" + str(p) +
                       "is successful")
            else:
                return(response.status_code)

        return(response.status_code)

    def getPortGroup(self):
        """Query the PortGroup id."""
        for p in range(0, 1):
            url = 'http://' + self.neutron_hostname + ':9696/' + self.osver + \
                  '/sfc/port_pair_groups?name=PG' + str(p)
            headers = {"Accept": "application/json", "X-Auth-Token":
                       self.token_id}
            response = requests.get(url, headers=headers)

            if (response.status_code == 200):
                self.logger.debug(response.status_code)
                self.logger.debug(response.content)
                json1_data = json.loads(response.content)
                self.port_grp_id.append(json1_data['port_pair_groups']
                                        [0]['id'])
            else:
                return(response.status_code)
        return(response.status_code)

    def createFlowClassifier(self):
        """Creation of Flow Classifier."""
        Dicdata = {}
        if self.source_ip_prefix != '':
            Dicdata['source_ip_prefix'] = self.source_ip_prefix
        if self.destination_ip_prefix != '':
            Dicdata['destination_ip_prefix'] = self.destination_ip_prefix
        if self.logical_source_port != '':
            Dicdata['logical_source_port'] = self.port_num[0]
        if self.fcname != '':
            Dicdata['name'] = "FC1"
        if self.ethertype != '':
            Dicdata['ethertype'] = self.ethertype

        Dicdata = {'flow_classifier': Dicdata}
        data = json.dumps(Dicdata, indent=4)
        url = 'http://' + self.neutron_hostname + ':9696/' + self.osver + \
              '/sfc/flow_classifiers'
        headers = {"Accept": "application/json",
                   "X-Auth-Token": self.token_id}
        response = requests.post(url, headers=headers,  data=data)
        if (response.status_code == 201):
            json1_data = json.loads(response.content)
            self.flow_class_if = json1_data['flow_classifier']['id']
            self.logger.info("\tCreation of Flow Classifier is successful")
            return(response.status_code)
        else:
            return(response.status_code)

    def createPortChain(self):
        """Creation of PortChain."""
        Dicdata = {}
        flow_class_list = []
        flow_class_list.append(self.flow_class_if)
        port_pair_groups_list = []
        port_pair_groups_list.append(self.port_grp_id[0])

        if flow_class_list != '':
            Dicdata['flow_classifiers'] = flow_class_list
        if self.pcname != '':
            Dicdata['name'] = "PC1"
        if port_pair_groups_list != '':
            Dicdata['port_pair_groups'] = port_pair_groups_list

        Dicdata = {'port_chain': Dicdata}
        data = json.dumps(Dicdata, indent=4)
        url = 'http://' + self.neutron_hostname + ':9696/' + self.osver + \
              '/sfc/port_chains'
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json",
                   "X-Auth-Token": self.token_id}
        response = requests.post(url, headers=headers,  data=data)
        if (response.status_code == 201):
            self.logger.info("\tCreation of PORT CHAIN is successful")
            json1_data = json.loads(response.content)
            self.PC_id = json1_data['port_chain']['id']
            return(response.status_code)
        else:
            return(response.status_code)

    def checkFlowAdded(self):
        """Check whether the Flows are downloaded successfully."""
        time.sleep(5)
        response = requests.get('http://' + self.onos_hostname +
                                ':8181/onos/v1/flows',
                                auth=("karaf",  "karaf"))
        if (response.status_code == 200):
            self.logger.info("\tFlow is successfully Queries")
            json1_data = json.loads(response.content)
            self.flowadd = json1_data['flows'][0]['state']

            if (self.flowadd == "ADDED"):
                self.logger.info("\tFlow is successfully added to OVS")
                return(response.status_code)
            else:
                return(404)
        else:
            return(response.status_code)
####################################################################

    def createRouter(self):
        """Creation of Router."""
        Dicdata = {}
        if self.routername != '':
            Dicdata['name'] = "router1"
        if self.admin_state_up != '':
            Dicdata['admin_state_up'] = self.admin_state_up

        Dicdata = {'router': Dicdata}
        data = json.dumps(Dicdata, indent=4)
        url = 'http://' + self.neutron_hostname + ':9696/' + \
            self.osver + '/routers.json'
        headers = {"Accept": "application/json",
                   "X-Auth-Token": self.token_id}
        response = requests.post(url, headers=headers,  data=data)
        if (response.status_code == 201):
            self.logger.debug(response.status_code)
            self.logger.debug(response.content)
            self.logger.info("\tCreation of Router is successfull")
            json1_data = json.loads(response.content)
            self.logger.debug(json1_data)
            self.router_id = json1_data['router']['id']
            return(response.status_code)
        else:
            return(response.status_code)

    def attachInterface(self):
        """Attachment of instance ports to the Router."""
        url = 'http://' + self.neutron_hostname + ':9696/' + self.osver + \
              '/networks?name=admin_floating_net'
        headers = {"Accept": "application/json",
                   "X-Auth-Token": self.token_id}
        response = requests.get(url, headers=headers)
        if (response.status_code == 200):
            self.logger.debug(response.status_code)
            self.logger.debug(response.content)
            json1_data = json.loads(response.content)
            self.logger.debug(json1_data)
            self.net_name = json1_data['networks'][0]['name']
            if (self.net_name == "admin_floating_net"):
                self.pub_net_id = json1_data['networks'][0]['id']
            else:
                return(response.status_code)
        ############################################################

        self.logger.info("\tAttachment of Instance interface to Router")
        Dicdata = {}
        if self.subnetId != '':
            Dicdata['subnet_id'] = self.subnetId

        data = json.dumps(Dicdata, indent=4)
        url = 'http://' + self.neutron_hostname + ':9696/' + self.osver + \
              '/routers/' + self.router_id + '/add_router_interface'
        headers = {"Accept": "application/json",
                   "X-Auth-Token": self.token_id}
        response = requests.put(url, headers=headers,  data=data)
        if (response.status_code == 200):
            self.logger.debug(response.status_code)
            self.logger.debug(response.content)
            self.logger.info("\tInterface attached successfull")
        else:
            return(response.status_code)
        ############################################################
        self.logger.info("\tAttachment of Gateway to Router")

        Dicdata1 = {}
        if self.pub_net_id != 0:
            Dicdata1['network_id'] = self.pub_net_id

        Dicdata1 = {'external_gateway_info': Dicdata1}
        Dicdata1 = {'router': Dicdata1}
        data = json.dumps(Dicdata1, indent=4)
        url = 'http://' + self.neutron_hostname + ':9696/' + self.osver + \
              '/routers/' + self.router_id
        headers = {"Accept": "application/json",
                   "X-Auth-Token": self.token_id}
        response = requests.put(url, headers=headers,  data=data)
        if (response.status_code == 200):
            self.logger.debug(response.status_code)
            self.logger.debug(response.content)
            self.logger.info("\tGateway Interface attached successfull")
            return(response.status_code)
        else:
            return(response.status_code)

    def addFloatingIp(self):
        """Attachment of Floating Ip to the Router."""
        for ip_num in range(0, 2):
            Dicdata = {}
            Dicdata['pool'] = "admin_floating_net"

            data = json.dumps(Dicdata, indent=4)
            url = 'http://' + self.nova_hostname + ':8774/v2.1/os-floating-ips'
            headers = {"Accept": "application/json",
                       "X-Auth-Token": self.token_id}
            response = requests.post(url, headers=headers,  data=data)
            if (response.status_code == 200):
                self.logger.debug(response.status_code)
                self.logger.debug(response.content)
                self.logger.info("\tFloating ip created successfully")
                json1_data = json.loads(response.content)
                self.logger.debug(json1_data)
                self.vm_public_ip.append(json1_data['floating_ip']['ip'])
                self.vm_public_id.append(json1_data['floating_ip']['id'])
            else:
                self.logger.error("\tFloating ip NOT created successfully")

            Dicdata1 = {}
            if self.address != '':
                Dicdata1['address'] = self.vm_public_ip[ip_num]

            Dicdata1 = {'addFloatingIp': Dicdata1}
            data = json.dumps(Dicdata1, indent=4)
            url = 'http://' + self.nova_hostname + ':8774/v2.1/servers/' + \
                  self.vm[ip_num] + '/action'
            headers = {"Accept": "application/json",
                       "X-Auth-Token": self.token_id}
            response = requests.post(url, headers=headers,  data=data)
            if(response.status_code == 202):
                self.logger.debug(response.status_code)
                self.logger.debug(response.content)
                self.logger.info("\tPublic Ip successfully added to VM")
            else:
                return(response.status_code)
        return(response.status_code)

    def loginToVM(self):
        """Login to the VM to check NSH packets are received."""
        queue1 = "0"

        def vm0():

            s = pxssh.pxssh()
            hostname = self.vm_public_ip[0]
            username = "cirros"
            password = "cubswin:)"
            s.login(hostname,  username,  password)
            s.sendline("ping -c 5 " + str(self.port_ip[2]))
            s.prompt()             # match the prompt

            ping_re = re.search("transmitted.*received",  s.before).group()
            x = re.split('\s+',  ping_re)
            if (x[1] >= "1"):
                self.logger.info("\tPing is Successfull")
            else:
                self.logger.info("\tPing is NOT Successfull")

        def vm1(queue1):
            s = pxssh.pxssh()
            hostname = self.vm_public_ip[1]
            username = "cirros"
            password = "cubswin:)"
            s.login(hostname,  username,  password)
            s.sendline('sudo ./firewall')
            s.prompt()
            output_pack = s.before

            if(output_pack.find("nshc") != -1):
                self.logger.info("\tThe packet has reached VM2 Instance")
                queue1.put("1")
            else:
                self.logger.info("\tPacket not received in Instance")
                queue1.put("0")

        def ping(ip, timeout=300):
            while True:
                time.sleep(1)
                self.logger.debug("Pinging %s. Waiting for response..." % ip)
                response = os.system("ping -c 1 " + ip + " >/dev/null 2>&1")
                if response == 0:
                    self.logger.info("Ping " + ip + " detected!")
                    return 0

                elif timeout == 0:
                    self.logger.info("Ping " + ip + " timeout reached.")
                    return 1
                timeout -= 1

        result0 = ping(self.vm_public_ip[0])
        result1 = ping(self.vm_public_ip[1])
        if result0 == 0 and result1 == 0:
            time.sleep(300)
            queue1 = Queue()
            p1 = Process(target=vm1,  args=(queue1, ))
            p1.start()
            p2 = Process(target=vm0)
            p2.start()
            p1.join(10)
            return (queue1.get())
        else:
            print("Thread didnt run")

    """##################################################################"""
    """ ########################  Stats Functions ################# #####"""

    def portChainDeviceMap(self):
        """Check the PC Device Stats in the ONOS."""
        response = requests.get('http://' + self.onos_hostname +
                                ':8181/onos/vtn/portChainDeviceMap/' +
                                self.PC_id, auth=("karaf", "karaf"))
        if (response.status_code == 200):
            self.logger.info("\tPortChainDeviceMap is successfully Queries")
            return(response.status_code)
        else:
            return(response.status_code)

    def portChainSfMap(self):
        """Check the PC SF Map Stats in the ONOS."""
        response = requests.get('http://' + self.onos_hostname +
                                ':8181/onos/vtn/portChainSfMap/' +
                                self.PC_id, auth=("karaf",  "karaf"))
        if (response.status_code == 200):
            self.logger.info("\tportChainSfMap is successfully Queries")
            return(response.status_code)
        else:
            return(response.status_code)

    """###################################################################"""

    def deletePortChain(self):
        """Deletion of PortChain."""
        url = 'http://' + self.neutron_hostname + ':9696/' + self.osver + \
              '/sfc/port_chains/' + self.PC_id
        headers = {"Accept": "application/json", "Content-Type":
                   "application/json", "X-Auth-Token": self.token_id}
        response = requests.delete(url, headers=headers)
        if (response.status_code == 200):
            self.logger.debug(response.status_code)
            self.logger.debug(response.content)
            return(response.status_code)
        else:
            return(response.status_code)

    def deleteFlowClassifier(self):
        """Deletion of Flow Classifier."""
        url = 'http://' + self.neutron_hostname + ':9696/' + self.osver + \
              '/sfc/flow_classifiers/' + self.flow_class_if
        headers = {"Accept": "application/json",
                   "X-Auth-Token": self.token_id}
        response = requests.delete(url, headers=headers)
        if (response.status_code == 200):
            self.logger.debug(response.status_code)
            self.logger.debug(response.content)
            return(response.status_code)
        else:
            return(response.status_code)

    def deletePortGroup(self):
        """Deletion of PortGroup."""
        for p in range(0, 1):
            url = 'http://' + self.neutron_hostname + ':9696/' + self.osver + \
                  '/sfc/port_pair_groups/' + self.port_grp_id[p]
            headers = {"Accept": "application/json", "X-Auth-Token":
                       self.token_id}
            response = requests.delete(url, headers=headers)
            if (response.status_code == 204):
                self.logger.debug(response.status_code)
                self.logger.debug(response.content)
                print ("\n\t\tPort " + self.port_grp_id[p] + "Deleted")
            else:
                return(response.status_code)
        return(response.status_code)

    def deletePortPair(self):
        """Deletion of Portpair."""
        for p in range(1,  2):
            url = 'http://' + self.neutron_hostname + ':9696/' + self.osver + \
                  '/sfc/port_pairs/' + self.port_pair_id[0]
            headers = {"Accept": "application/json",
                       "X-Auth-Token": self.token_id}
            response = requests.delete(url, headers=headers)
            if (response.status_code == 204):
                self.logger.debug(response.status_code)
                self.logger.debug(response.content)
            else:
                return(response.status_code)
        return(response.status_code)

    def cleanup(self):
        """Cleanup."""
        print ("\n\t\tDeleting the VMs")
        for y in range(0, 3):
            url = 'http://' + self.nova_hostname + \
                ':8774/v2.1/servers/' + self.vm[y]
            headers = {"Accept": "application/json",
                       "X-Auth-Token": self.token_id}
            response = requests.delete(url, headers=headers)
            if (response.status_code == 204):
                self.logger.debug(response.status_code)
                self.logger.debug(response.content)
                print ("\n\t\tVM" + str(y) + " is Deleted : ")
                time.sleep(10)
            else:
                return(response.status_code)
        print ("\n\t\tDeletion of Ports")
        for x in range(self.i, self.numTerms):
            url = 'http://' + self.neutron_hostname + ':9696/' + self.osver + \
                  '/ports/' + self.port_num[x]
            headers = {"Accept": "application/json", "X-Auth-Token":
                       self.token_id}
            response = requests.delete(url, headers=headers)

            if (response.status_code == 204):
                self.logger.debug(response.status_code)
                self.logger.debug(response.content)
                print ("\n\t\tPort" + str(x) + "  Deleted")
            else:
                return(response.status_code)
        print ("\n\t\tDeleting Router")

        Dicdata = {}
        Dicdata['external_gateway_info'] = {}
        Dicdata = {'router': Dicdata}
        data = json.dumps(Dicdata, indent=4)
        url = 'http://' + self.neutron_hostname + ':9696/' + self.osver + \
              '/routers/' + self.router_id
        headers = {"Accept": "application/json",
                   "X-Auth-Token": self.token_id}
        response = requests.put(url, headers=headers,  data=data)
        if (response.status_code == 200):
            self.logger.debug(response.status_code)
            self.logger.debug(response.content)
            Dicdata1 = {}
            if self.subnetId != '':
                Dicdata1['subnet_id'] = self.subnetId
            data = json.dumps(Dicdata1, indent=4)
            url = 'http://' + self.neutron_hostname + ':9696/' + self.osver + \
                  '/routers/' + self.router_id + \
                  '/remove_router_interface.json'
            headers = {"Accept": "application/json",
                       "X-Auth-Token": self.token_id}
            response = requests.put(url, headers=headers,  data=data)
            if (response.status_code == 200):
                url = ('http://' + self.neutron_hostname + ':9696/' +
                       self.osver + '/routers/' + self.router_id)
                headers = {"Accept": "application/json",  "X-Auth-Token":
                           self.token_id}
                response = requests.delete(url, headers=headers)
                if (response.status_code == 204):
                    self.logger.debug(response.status_code)
                    self.logger.debug(response.content)
                    print ("\n\t\tDeletion of Router is successfull")
                else:
                    return(response.status_code)
            else:
                return(response.status_code)
        else:
            return(response.status_code)

        print ("\n\t\tDeletion of Network")
        url = 'http://' + self.neutron_hostname + ':9696/' + self.osver + \
              '/networks/' + self.net_id
        headers = {"Accept": "application/json",
                   "X-Auth-Token": self.token_id}
        response = requests.delete(url, headers=headers)
        if (response.status_code == 204):
            self.logger.debug(response.status_code)
            self.logger.debug(response.content)
            print ("\n\t\tNetwork deleted Successfully")
        else:
            return(response.status_code)

        print ("\n\t\tDeletion of Floating ip")
        for ip_num in range(0, 2):
            url = 'http://' + self.neutron_hostname + ':9696/' + self.osver + \
                  '/floatingips/' + self.vm_public_id[ip_num]
            headers = {"Accept": "application/json", "X-Auth-Token":
                       self.token_id}
            response = requests.delete(url, headers=headers)
            if (response.status_code == 204):
                self.logger.debug(response.status_code)
                self.logger.debug(response.content)
            else:
                return(response.status_code)
        return(response.status_code)
