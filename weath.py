#!/usr/bin/env python
import libfann
import re
import random

error = 0.0001
max_iter = 10000
iter_betw_repor = 1000
ann = libfann.neural_net()
ann.set_training_algorithm(libfann.TRAIN_RPROP)
ann.set_activation_function_output(libfann.LINEAR)
ann.create_standard_array([5,5,1])

count = ''
with open("weather.txt","r")  as f:
        count = f.read().strip().replace('\n',' ').replace('\r','')
        count = re.sub('\s+', ' ', count)
#print(count.split(' '))        
data = [int(c) for c in count.split(' ') ]
vec = []
res = []
N = 5

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
#print(len(vec_train),len(res_train))

tr_data = libfann.training_data()
tr_data.set_train_data([[0,0,0,0,0]],[[0]])
print(tr_data)
ann.train_on_data(tr_data,max_iter,iter_betw_repor,error)
ann.save("wdata_test.txt")
