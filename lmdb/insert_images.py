#! /usr/bin/env python

import lmdb
import sys
import os

env = lmdb.open("images", map_size=1024*1024*50)

txn = env.begin(write=True)

img = sys.argv[1]

keyName = os.path.basename(img)
data = ""
with open(img, 'r') as imgFile:
	data = imgFile.read();

txn.put(keyName, data, dupdata=False, overwrite=False)

print("Inserted:", img)

txn.commit()
