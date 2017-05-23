#!/usr/bin/python

import sys
import datetime



filename = sys.argv[1]
entrynum = sys.argv[2]
starttime = sys.argv[3]
endtime = sys.argv[4]

print filename + "  " + entrynum + " " + starttime + " " + endtime

str = """ ------------------------------------------------------------------------
Operation=throttle.protocolrework.businessmetrics.FilesystemMetrics.businessMetrics
Marketplace=dev-jianjin.us-east-1.adam
Program=MagnolioThrottleService
HostGroup=us-east-1a
Hostname=10.1.24.216
fsId=fs-00000000
ownerAcct=
Time=0.000 ms
EndTime=
StartTime=
Counters=OperationCount=1
Metrics=AVG.BASELINE.RATE.MiBPS=0.049 acct|150865063228 fs|fs-00000000 AZ|IAD12,AVG.MAX.BANDWIDTH.MiBPS=100.0 acct|150865063228 fs|fs-00000000 AZ|IAD12,MIN.MAX.BANDWIDTH.MiBPS=100.0 AZ|IAD12,MAX.BASELINE.RATE.MiBPS=0.049 AZ|IAD12,EMIT_METRIC.COUNT=1.0 AZ|IAD12,MAX.MAX.BANDWIDTH.MiBPS=100.0 AZ|IAD12,MIN.EXPECTED.BURST.RATE.MiBPS=100.0 AZ|IAD12,MAX.EXPECTED.BURST.RATE.MiBPS=100.0 AZ|IAD12,MAX.BURST.CREDIT.BALANCE=2308974418330.0 AZ|IAD12,AVG.EXPECTED.BURST.RATE.MiBPS=100.0 acct|150865063228 fs|fs-00000000 AZ|IAD12,AVG.BURST.CREDIT.BALANCE=2308974418095.6 acct|150865063228 fs|fs-00000000 AZ|IAD12,MIN.BURST.CREDIT.BALANCE=2308974417754.0 AZ|IAD12,OperationLatency=0.197 ms,MIN.BASELINE.RATE.MiBPS=0.049 AZ|IAD12
EOE
"""




f = open(filename, 'a')

for num in range (1, int(entrynum)):
    s = "fs-%08d" % num
    result = str.replace("fs-00000000", s)
    result = result.replace("150865063228", s)
    result = result.replace("StartTime=", "StartTime="+starttime);
    result = result.replace("EndTime=", "StartTime="+endtime);
    result = result.replace("ownerAcct=", "ownerAcct="+s);
    f.write(result)

f.close() 

#sudo python service.py service_log.2017-03-23-20-20 10000 1490301930.111 "Thu, 23 Mar 2017 20:45:30 UTC"