#!/usr/bin/python

import sys
from datetime import datetime,timedelta

time=str(sys.argv[1])

secs=sum(x * float(t) for x, t in zip([3600, 60, 1], time.split(":"))) 

t=int((secs-10)//10)
ss=""
tt = datetime.strptime("00:00:00","%H:%M:%S")
for i in range(1,11):
	ttemp = tt + timedelta(seconds=(i*t))
	print ttemp.strftime("%H:%M:%S")