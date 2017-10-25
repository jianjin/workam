import os
import fcntl
import struct
import io
import time

FP = os.open("log_lock_0113157846", os.O_WRONLY | os.O_DIRECT)

LOCK_OFFSET = 0
# create lock
lockdata = struct.pack('hhllhh', fcntl.F_WRLCK, os.SEEK_SET, LOCK_OFFSET, 0, 0, 0)
fcntl.fcntl(FP, fcntl.F_SETLK, lockdata)

raw_input("Press any key")


#write data to it

with io.open("log_lock_0113157846", 'a') as f:
      for num in xrange(1000):
        f.write(u'bingo---------------------------------------------'+
      	    '9999999o--------------------------------------------------\n')
        if num % 100 == 0: 
           time.sleep(1)
           print("writing... %s" % num )


# check for locks
lockdata = struct.pack('hhllhh', fcntl.F_WRLCK, os.SEEK_SET, LOCK_OFFSET, 0, 0, 0)
fcntl.fcntl(FP, fcntl.F_GETLK, lockdata)

# remove lock
lockdata = struct.pack('hhllhh', fcntl.F_UNLCK, os.SEEK_SET, LOCK_OFFSET, 0, 0, 0)
fcntl.fcntl(FP, fcntl.F_SETLK, lockdata)

os.close(FP)
