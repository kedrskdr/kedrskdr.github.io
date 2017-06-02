#!/usr/bin/env python

import subprocess
from matplotlib import pyplot
import math
import pylab
from matplotlib import mlab
import sys
import random
output = []

max_acc = 0.0
#for N in range(mn,mx,dx):
for i in range(5):
	H = random.randrange(20,150)
	ITER = random.randrange(50,500)*10
	LR = (random.randrange(0,100)*1.0)/100.0
	WEI = (random.randrange(0,100)*1.0)/100.0
	for ii in range(3):
		try:
			tmp = subprocess.Popen(["/home/eugenia/kedrskdr.github.io/pr_k2.py",str(H),str(ITER),str(LR),str(WEI)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#			print tmp.stderr.read()
			aaaaa = tmp.stdout.read()
#			print aaaaa
			tmp = aaaaa.split("\n")[-2]
		except subprocess.CalledProcessError as e:
			print e.returncode
			print e.output
			tmp = e.output
			print tmp.stderr.read()
		sys.stderr.write("%d %d \n" %(H,i)) 
#		print tmp.stderr.read()
#		print "tmp", tmp, "\n"
#		print "tmp-2",tmp[-2]
#		output.append((tmp))
		mas_tmp= tmp.split(" ")
#		mas_tmp = output.split(" ")	
		print mas_tmp
#		mas_tmp = tmp
#		print max_acc, mas_tmp[0],mas_tmp[1],mas_tmp[2],mas_tmp[3]
	

	
		if max_acc < float(mas_tmp[3]):
			max_acc = float(mas_tmp[3])
			print "New max ",H,ITER,LR,WEI,mas_tmp[2],max_acc	
	

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
