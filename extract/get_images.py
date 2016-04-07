#! /usr/bin/env python

import lmdb

env = lmdb.open("images_db", readonly=True)

txn = env.begin()

cursor = txn.cursor()

for key, value in cursor:
	print key
        print value
        break
