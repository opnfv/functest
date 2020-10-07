import paramiko
import os
import time

from functest.opnfv_tests.rbdbench import rbdbench

class StorageValidation:

    def execute(self):
        commands = open("commands.yaml", "r")
        for i in commands.readlines():
            l = i.strip()
            rbd_command = l.split(",")
        p = paramiko.SSHClient()
        cred = open("cred.yaml", "r")
        for i in cred.readlines():
            line = i.strip()
            ls = line.split(",")
            p.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                p.connect("%s" % ls[0], username="%s" % ls[1], password="%s" % ls[2])
                print("Connected to Storage Client")
            except:
                print("[!] Cannot connect to the SSH Server")
                exit()
            for command in rbd_command:
                print("=" * 100)
                stdin, stdout, stderr = p.exec_command(command)
                opt = stdout.readlines()
                opt = "".join(opt)
                print(opt)
                var = time.strftime("%d%m%y%H%M%S")
                temp = open("output_%s.txt" % var, "a")
                temp.write(opt)
                temp.close()
        cred.close()
        commands.close()