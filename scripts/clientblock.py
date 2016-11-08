import os
import fcntl
import struct
import time


def nanoTime():
    return int(round(time.time() * 1000000))


for j in xrange(1000):
  
    print "\nopen lock unlock close :"+str(j)
    print " "+str(nanoTime())
    for i in xrange(100):
        fp = os.open("locktest/jj/file_"+str(j), os.O_WRONLY | os.O_DIRECT)
          
             # create lock
        lockdata = struct.pack('hhllhh', fcntl.F_WRLCK, os.SEEK_SET, lock_offset, 1, 0, 0)
        fcntl.fcntl(fp, fcntl.F_SETLK, lockdata)
         
        lockdata = struct.pack('hhllhh', fcntl.F_UNLCK, os.SEEK_SET, lock_offset, 1, 0, 0)
        fcntl.fcntl(fp, fcntl.F_SETLK, lockdata)
         
        os.close(fp)
    print " "+str(nanoTime())


