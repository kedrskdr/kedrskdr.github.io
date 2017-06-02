#!/usr/bin/env python
from fann2 import libfann
import re
import random
import sys

#NN = [int(i) for i in range(4,11)]
N = int(sys.argv[1]) 
H = int(sys.argv[2])

error = 0.000001
max_iter = 300
iter_betw_repor = 100
ann = libfann.neural_net()
ann.create_standard_array([N,H,1])
ann.set_learning_rate(0.5)
ann.set_training_algorithm(libfann.TRAIN_RPROP)
ann.set_activation_function_output(libfann.SIGMOID)
ann.set_activation_function_hidden(libfann.SIGMOID_SYMMETRIC)

count = ''
data = []
ext = []
virus_count  = 0
clear_count = 0
#nnn=100000
for ss in  open("in_test0.txt","r"):
	dat  = map(int,ss.strip().replace('\n', '').replace('\r', '').split(','))
	data.append(dat[:-1])
	ext.append(dat[-1:])
#		nnn-=1
#		if nnn == 0:
#		break
#for i in range (len(data)):
#	data[i] = (data[i] - sr)/(1.0*srotkl)	


ann.randomize_weights(-1,1)

#for i in range (len(data)-N-1):
 #      	vec.append(data[i:i+N])
  #     	res.append([data[i+N+1]])

indvec = range(len(data))
random.shuffle(indvec)
#print(len(indvec))
#print("indvec",indvec)
vec_train = [data[i] for i in indvec[:int(len(data)*0.8)]]
res_train = [ext[i] for i in indvec[:int(len(data)*0.8)]]
vec_test = [data[i] for i in indvec[int(len(data)*0.8):]]
res_test = [ext[i] for i in indvec[int(len(data)*0.8):]]
#print(len(vec_train),len(res_train))"
#print vec_train

#print len(data)
#print len(ext)
tr_data = libfann.training_data()
tr_data.set_train_data(vec_train,res_train)
#print(vec_train)
ann.train_on_data(tr_data,max_iter,iter_betw_repor,error)
thr = 0.0
auc = 0.0
last_fpr = 0
last_tpr = 0
max_acc = 0.0
for p in range(0,1001):
	 #0.1....0.9 postrROP
	(fp,tp,fn,tn) = (0,0,0,0) # hypothises is this vector is from malicious process
#run on test sample
	for i in range(len(vec_test)):
		bbb = ann.run(vec_test[i])
		if res_test[i][0] == 1.0:
			if bbb[0] > thr:
				tp+=1
			else :
				fn+=1
		else:
			if bbb[0] > thr:	
				fp+=1
			else:
				tn+=1
	acc = (tp + tn)/(1.0*len(vec_test))
#	print acc:
#	print thr,acc,auc,tp/((tp+tn)*1.0),fp/((fp+tn)*1.0),'\r'
#	print fp, tp, fn, tn
	fpr = fp/((fp+tn)*1.0)
	
	if tp+tn == 0:	
		tpr = 0
	else:	
		tpr = tp/((tp+tn)*1.0)
	if p>0:
		auc += (fpr+last_fpr)*(last_tpr-tpr)/2.0
	last_fpr = fpr
	last_tpr = tpr
#	print "%f\t%f" %(tpr,fpr)
	thr += 0.001
	if max_acc < acc:
		max_acc = acc

#print tpr,fpr
	print N,H,auc,max_acc




"""
err = 0
testt = []
for i in range (len(vec_test)):
	comp = ann.run(vec_test[i])[0]
#	print comp*srotkl+sr,res_test[i][0]*srotkl+sr
		testt.append(res_test[i][0]*srotkl+sr)
	err += (comp - res_test[i][0])**2
	#print(testt[i])
err_mas.append(err)
print (err)
#print (N)
#print (err_mas)
#print (NN)

#ann.save("wdata_test.txt")

"""
