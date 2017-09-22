import sys
from config import *
from vm2docker import *

dockerimg = sys.argv[1]
vfile = sys.argv[2]
vmguser = sys.argv[3]
vmgpasswd = sys.argv[4]

if __name__ == "__main__":
    vm2docker = VM2Docker(vfile, vmguser, vmgpasswd)
    vm2docker.run(dockerimg)
    