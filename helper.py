import logger
import subprocess

def run(cmd):
    logger.info(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = []
    while True:
        line = p.stdout.readline()
        stdout.append(line)
        logger.info(line)
        if line == '' and p.poll() != None:
            break
    
    return ''.join(stdout)

