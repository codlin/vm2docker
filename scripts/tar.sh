#! /bin/bash

cd /
rm -f docker2vm_img.tar
tar cf /docker2vm_img.tar --exclude=/docker2vm_img.tar --one-file-system /
