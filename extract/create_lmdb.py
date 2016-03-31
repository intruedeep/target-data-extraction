import lmdb
env = lmdb.open("images_db", map_size=1024*1024*50)
txn = env.begin(write=True)
txn.commit()
