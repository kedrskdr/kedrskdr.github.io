#!/usr/bin/env python

import subprocess
from matplotlib import pyplot
import math
import pylab
from matplotlib import mlab
import sys
output = []
N = 10
mn = 20 
mx = 100
dx = 10
mn1 = 40
mx1 = 100
dx1 = 10
#tmp = []
x = []
y = []
max_acc = 0.0
#for N in range(mn,mx,dx):
for H in range(mn1,mx1,dx1):
	for i in range(5):
		tmp = subprocess.check_output(["/home/eugenia/kedrskdr.github.io/tet.py",str(N),str(H)]).split('\n')[-2]

		output.append((tmp,N,H))
		mas_tmp= tmp.split(" ")
#			print tmp
		if max_acc < float(mas_tmp[1]):
			max_acc = float(mas_tmp[1])
			print N,H,mas_tmp[0],max_acc	
		



		#	y.append(float(tmp))
		#	x.append((N,H))		
"""table = {}
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
print x,y
xx  = [i for i in range(1,len(y)+1)]
print xx
pylab.plot(xx,y)
pylab.show()
"""
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
