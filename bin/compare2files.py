#!/usr/bin/python

import sys
file1 = sys.argv[1]
file2 = sys.argv[2]
try:
	file1lines = open(file1).readlines()
except:
	print file1lines
	exit(0)
file2lines = open(file2).readlines()

for line in file1lines:
	if line in file2lines:
		continue
	else:
		print line.replace("\n","")
