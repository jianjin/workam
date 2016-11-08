import os
import fcntl
import struct

fp = os.open("/mnt/lock_file", os.O_WRONLY | os.O_DIRECT)

# create lock
lockdata = struct.pack('hhllhh', fcntl.F_WRLCK, os.SEEK_SET, lock_offset, 1, 0, 0)
fcntl.fcntl(fp, fcntl.F_SETLK, lockdata)

raw_input("Press any key")

# check for locks
lockdata = struct.pack('hhllhh', fcntl.F_WRLCK, os.SEEK_SET, 1, 1, 0, 0)
fcntl.fcntl(fp, fcntl.F_GETLK, lockdata)

# remove lock
lockdata = struct.pack('hhllhh', fcntl.F_UNLCK, os.SEEK_SET, lock_offset, 1, 0, 0)
fcntl.fcntl(fp, fcntl.F_SETLK, lockdata)

os.close(fp)
