import time
import paramiko

from functest.opnfv_tests.rbdbench import rbdbench

class StorageValidation:

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
                print("Connected to Storage Client")
            except:
                print("[!] Cannot connect to the SSH Server")
                exit()
            for command in rbd_command:
                print("=" * 100)
                stdin, stdout, stderr = Client.exec_command(command)
                opt = stdout.readlines()
                opt = "".join(opt)
                print(opt)
                var = time.strftime("%d%m%y%H%M%S")
                temp = open("output_%s.txt" % var, "a")
                temp.write(opt)
                temp.close()
        cred.close()
        commands.close()
