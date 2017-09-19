import os
import sys
import time
from helper import *

vmg_run = {
    'exiterr': 'Guest program exited with non-zero exit code',
}

class VMWare(object):
    def __init__(self, vmx, vmuser, vmpasswd):
        '''
        vmx: the VMX path for VMWare images
        '''
        self.vmx = vmx
        if not os.path.exists(vmx):
            raise IOError("vmx path {} doesn't exist.".format(vmx))
            sys.exit(1)
        
        self.vmuser = vmuser
        self.vmpasswd = vmpasswd
    
    def start(self):
        cmd = "vmrun -T ws start {} nogui".format(self.vmx)
        res = run(cmd)
        if 'Error' in res:
            logger.critical("start vm guest failed, exit.")
            sys.exit(1)
            
        logger.info("wait a while for VM starting...")
        time.sleep(180)

    def stop(self):
        cmd = "vmrun -T ws stop {} nogui".format(self.vmx)
        run(cmd)
    
    def cpfiletoguest(self, source, target):
        cmd = "vmrun -T ws -gu {} -gp {} CopyFileFromHostToGuest \"{}\" {} {}".format(self.vmuser, self.vmpasswd, self.vmx, source, target)
        run(cmd)
    
    def cpfilefromguest(self, source, target):
        cmd = "vmrun -T ws -gu {} -gp {} CopyFileFromGuestToHost \"{}\" {} {}".format(self.vmuser, self.vmpasswd, self.vmx, source, target)
        run(cmd)

    def runscriptinguest(self, exe, script):
        cmd = "vmrun -T ws -gu {} -gp {} runScriptInGuest \"{}\" {} {}".format(self.vmuser, self.vmpasswd, self.vmx, exe, script)
        result = run(cmd)
        if vmg_run.get('exiterr') in result:
            logger.error("run command get failed.")
            return (False, result)
        
        return (True, result)
