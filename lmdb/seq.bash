#! /usr/bin/env bash

set -o posix

# images should be stored in a subdirectory specified below
imgDir='jpgs'
commonImgName='frame'
imgType='jpg'
numImages=$(ls -l ${imgDir} | grep -v "total" | wc -l)

for ((i = 0; i < numImages; i++))
do
	./insert_images.py ${imgDir}/${commonImgName}${i}.${imgType}
done
