import os
import sys
import stat
import pexpect
from vm import *

root_dir = os.path.dirname(os.path.abspath(__file__))
docker_dir = os.path.join(root_dir, "dockerfiles")
scripts_dir = os.path.join(root_dir, "scripts")

class VM2Docker(object):
    def __init__(self, vmx, vmuser, vmpasswd):
        self.vm = VMWare(vmx, vmuser, vmpasswd)
    
    def run(self, imgname='vm2docker:raw'):
        self._getimg()
        cmd = pexpect.spawn("cd {}".format(docker_dir))
        cmd.logfile = sys.stdout
        cmd.sendline("docker build -t {} .".format(imgname))
        cmd.expect("# ")
    
    def _getimg(self):
        self.vm.start()

        tar = os.path.join(scripts_dir, "tar.sh")
        os.chmod(tar, stat.S_IXGRP)
        self.vm.cpfiletoguest(tar, "/tar.sh")
        status, res = self.vm.runscriptinguest("/bin/sh", "/tar.sh")
        if status is False:
            logger.error("tar / failed. please check your vm guest whether has enough disk space left.")
            sys.exit(1)

        self.vm.cpfilefromguest("/docker2vm_img.tar", os.path.join(docker_dir, "docker2vm_img.tar")
        if not os.path.exists("{}/docker2vm_img.tar".format(docker_dir)):
            logger.error("get docker2vm_img.tar from vm guest failed.")
            sys.exit(1)
