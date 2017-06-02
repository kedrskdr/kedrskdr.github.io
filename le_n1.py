#!/usr/bin/env python

import subprocess
from matplotlib import pyplot
import math
import pylab
from matplotlib import mlab
import sys
output = []

mn = 5
mx = 20
dx = 2
mn1 = 10
mx1 = 100
dx1 = 10
#tmp = []
x = []
y = []

for N in range(mn,mx,dx):
	for H in range(mn1,mx1,dx1):
		for i in range(50):
			tmp = subprocess.check_output(["/home/eugenia/kedrskdr.github.io/weath.py",str(N),str(H)]).split('\n')[3]

			output.append((float(tmp),N,H))
		#	y.append(float(tmp))
		#	x.append((N,H))		
table = {}
for i in output:
	if (i[1],i[2]) in table :
		if table[(i[1],i[2])] > i[0]:
			table[(i[1],i[2])] = i[0]
	else:
		table[(i[1],i[2])] = i[0]	
for i in range(mn1,mx1,dx1):
	sys.stdout.write(str(i) + "\t")
print "\r"
for N in range(mn,mx,dx):
	sys.stdout.write(str(N)+"\t")
	for H in range(mn1,mx1,dx1):
		sys.stdout.write(str(table[(N,H)]).replace(".", ",")+"\t")
	print "\r"

#print "\t".join([str(c).replace(".",",") for c in i])
"""print x,y
xx  = [i for i in range(1,len(y)+1)]
print xx
pylab.plot(xx,y)
pylab.show()"""
#print output
#for i in range(len(output)):
#	print output[i] 


#t = output[0]
#for i in output:
#	if i[0] < t[0]:
#		t = i
#print t




#end  = [output[i] for i in range(3,len(output),5)]

#for i in range (len(end)):
#	print end[i]

#print min(end) """
