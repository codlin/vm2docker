import os
import sys
import stat
from vm import *
from helper import *

root_dir = os.path.dirname(os.path.abspath(__file__))
docker_dir = os.path.join(root_dir, "dockerfiles")
scripts_dir = os.path.join(root_dir, "scripts")

class VM2Docker(object):
    def __init__(self, vfile, vmuser, vmpasswd):
        vmx = self._convertvftovmx(vfile)
        self.vm = VMWare(vmx, vmuser, vmpasswd)
    
    def __del__(self):
        if isinstance(self.vm, VMWare):
            logger.info("stop vmware guest: {}".format(self.vm.vmx))
            self.vm.stop()
        
    def run(self, imgname='vm2docker:raw'):
        if imgname is None or imgname == '':
            imgname = 'vm2docker:raw'
        
        self.vm.start()

        self._getimg()

        cmd = "docker build -t {} {} ".format(imgname, "dockerfiles")
        run(cmd)
    
    def _getimg(self):
        tar = os.path.join(scripts_dir, "tar.sh")
        os.chmod(tar, stat.S_IXGRP)
        self.vm.cpfiletoguest(tar, "/tar.sh")
        status, res = self.vm.runscriptinguest("/bin/sh", "/tar.sh")
        if status is False:
            logger.error("tar / failed. please check your vm guest whether has enough disk space left.")
            sys.exit(1)

        self.vm.cpfilefromguest("/docker2vm_img.tar", os.path.join(docker_dir, "docker2vm_img.tar"))
        if not os.path.exists("{}/docker2vm_img.tar".format(docker_dir)):
            logger.error("get docker2vm_img.tar from vm guest failed.")
            sys.exit(1)
    
    def _convertvftovmx(self, vfile):
        file, suffix = os.path.splitext(vfile)
        if suffix not in ['.ova', '.ovf', '.vmx']:
            raise TypeError("Unsupport VM type {}.".format(file))
            sys.exit(1)
        
        vmx = "{}_new.vmx".format(file)
        if suffix != '.vmx':
            cmd = "ovftool -tt=VMX {} {}".format(vfile, vmx)
            run(cmd)
        
        return vmx