#!/usr/bin/env python

import subprocess
from matplotlib import pyplot
import math
import pylab
from matplotlib import mlab
import sys
output = []
N = 4
H=10
 

mn1 = 10
mx1 = 150
dx1 = 10
#tmp = []
x = []
y = []
max_acc = 0.0
#for N in range(mn,mx,dx):
for H in range(mn1,mx1,dx1):
	for i in range(3):
		tmp = subprocess.check_output(["/home/eugenia/kedrskdr.github.io/pr_k1.py",str(N),str(H)]).split('\n')[-2]
		sys.stderr.write("%d %d \n" %(H,i)) 
#		print "tmp", tmp, "\n"
#		print "tmp-2",tmp[-2]
#		output.append((tmp))
		mas_tmp= tmp.split(" ")
#		mas_tmp = output.split(" ")	
#		print mas_tmp
#		print "one element", mas_tmp[2]
#		mas_tmp = tmp
#		print max_acc, mas_tmp[0],mas_tmp[1],mas_tmp[2],mas_tmp[3]
	
		
	
		
	
		if max_acc < float(mas_tmp[3]):
			max_acc = float(mas_tmp[3])
			print N,H,mas_tmp[2],max_acc	
	"""	


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
print x,y
xx  = [i for i in range(1,len(y)+1)]
print xx
pylab.plot(xx,y)
pylab.show()

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

#print min(end)
 """
