import sys
from config import *
from vm2docker import *

if __name__ == "__main__":
    vm2docker = VM2Docker(VMGCF['vmx'], VMGCF['vmguser'], VMGCF['vmgpasswd'])
    vm2docker.run(imgname=sys.argv[1])
    