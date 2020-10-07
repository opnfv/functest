import logging
import time
import paramiko

from functest.opnfv_tests.rbdbench import rbdbench

class StorageValidation:

    LOGGER = logging.getLogger(__name__)

    def execute(self):
        commands = open("commands.yaml", "r")
        for i in commands.readlines():
            Line = i.strip()
            rbd_command = Line.split(",")
        Client = paramiko.SSHClient()
        cred = open("cred.yaml", "r")
        for i in cred.readlines():
            line = i.strip()
            String = line.split(",")
            Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                Client.connect("%s" % String[0], username="%s" % String[1], password="%s" % String[2])
                self.LOGGER.info("Connected to Storage Client")
            except:
                self.LOGGER.error("[!] Cannot connect to the SSH Server")
                exit()
            for command in rbd_command:
                stdin, stdout, stderr = Client.exec_command(command)
                opt = stdout.readlines()
                opt = "".join(opt)
                self.LOGGER.info("%s\n%s", opt)
                var = time.strftime("%d%m%y%H%M%S")
                temp = open("output_%s.txt" % var, "a")
                temp.write(opt)
                temp.close()
        cred.close()
        commands.close()
