#! /usr/bin/env python

import lmdb

env = lmdb.open("images", readonly=True)

txn = env.begin()

cursor = txn.cursor()

for key, value in cursor:
	print key
