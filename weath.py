#!/usr/bin/env python
from fann2 import libfann
import re
import random
import sys

NN = [int(i) for i in range(4,11)]
err_mas = []
#N=int(sys.argv[1])
for i in range(4,11):
	N=i

	error = 0.000001
	max_iter = 1000
	iter_betw_repor = 100000
	ann = libfann.neural_net()
	ann.create_standard_array([N,1,1])
	ann.set_learning_rate(0.5)
	ann.set_training_algorithm(libfann.TRAIN_RPROP)
	ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC)
	ann.set_activation_function_hidden(libfann.SIGMOID_SYMMETRIC)

	count = ''
	with open("weather.txt","r")  as f:
        	count = f.read().strip().replace('\n',' ').replace('\r','')
        	count = re.sub('\s+', ' ', count)
#print(count.split(' '))        
	data = [int(c) for c in count.split(' ') ]
	i=0
	s=0.0
#zentrirovanie
	max = data[0]
	for i in range (len(data)):
		if data[i] > max:
			max = data[i]

	for i in range (len(data)):
		s+=data[i]
		sr = s/(1.0*len(data))
	srotkl = 0
	for i in data:
		srotkl = srotkl + (i-sr)*(i-sr)
	import math
	srotkl = math.sqrt(srotkl)
#print (s)
	summ = 0	
	for i in range (len(data)):
		data[i] = (data[i] - sr)/(1.0*srotkl)	

	ann.randomize_weights(-1,1)
	vec = []
	res = []

	for i in range (len(data)-N-1):
        	vec.append(data[i:i+N])
        	res.append([data[i+N+1]])

	indvec = range(len(vec))
	random.shuffle(indvec)
#print(len(indvec))
#print("indvec",indvec)
	vec_train = [vec[i] for i in indvec[:int(len(data)*0.8)]]
	res_train = [res[i] for i in indvec[:int(len(data)*0.8)]]
	vec_test = [vec[i] for i in indvec[int(len(data)*0.8):]]
	res_test = [res[i] for i in indvec[int(len(data)*0.8):]]
#print(len(vec_train),len(res_train))"
#print vec_train
	tr_data = libfann.training_data()
	tr_data.set_train_data(vec_train,res_train)
#print(vec_train)
	ann.train_on_data(tr_data,max_iter,iter_betw_repor,error)
	err = 0
	testt = []

	for i in range (len(vec_test)):
		comp = ann.run(vec_test[i])[0]
#		print comp*srotkl+sr,res_test[i][0]*srotkl+sr
		testt.append(res_test[i][0]*srotkl+sr)
		err += (comp - res_test[i][0])**2
	#print(testt[i])
	err_mas.append(err)
	print (err)
	print (N)
print (err_mas)
print (NN)

ann.save("wdata_test.txt")
