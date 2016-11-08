import os
import fcntl
import struct
import time

latencylist = []

def nanoTime():
	return int(round(time.time() * 1000000))

def lockUnlockClose(fp):
    
    start = lstart = nanoTime()
    lock_offset = 0
    lockdata = struct.pack('hhllhh', fcntl.F_WRLCK, os.SEEK_SET, lock_offset, 1, 0, 0)
    fcntl.fcntl(fp, fcntl.F_SETLK, lockdata)
    lend = nanoTime()
    lockT = lend - lstart

    lbegin = nanoTime();
    lockdata = struct.pack('hhllhh', fcntl.F_UNLCK, os.SEEK_SET, lock_offset, 1, 0, 0)
    fcntl.fcntl(fp, fcntl.F_SETLK, lockdata)
    lend = nanoTime();
    unlockT = lend - lbegin

    lbegin = nanoTime();
    os.close(fp)
    lend = nanoTime();
    closeT = lend - lbegin

    latencylist.append((start, lockT, unlockT, closeT))

def runTest(numberoffiles, loopeachfile):
    for j in xrange(numberoffiles):
        for i in xrange(loopeachfile):
            fp = os.open("efs/lockunlockclose/file_"+str(j), os.O_WRONLY | os.O_DIRECT)
            try:
                lockUnlockClose(fp)
            except Exception as e :
                print e.__doc__
                print e.message
                continue
            # finally:
            #     if not fp.isClosed():
            #         os.close(fp)



def printResult():
    f = open('latencies-' + str(nanoTime()), 'a')
    f.write("timestamp,lock,ulock,close\n")
    print "Wring "+str(len(latencylist))+" to result file" + str(f)
    for timestamp, lock, unlock, close in latencylist:
        f.write( str(timestamp) + "," + str(lock) + "," + str(unlock) + "," +str(close)+"\n")
    f.close()

runTest(100,1)
printResult();


