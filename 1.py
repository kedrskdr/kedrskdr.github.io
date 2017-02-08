#!/usr/bin/env python
from pyfann import libfann 

error = 0.0001
max_iter = 10000
iter_betw_repor = 1000
ann = libfann.neural_net()
ann.set_training_algorithm(libfann.TRAIN_RPROP)
ann.set_activation_function_output(libfann.SIGMOID)
ann.set_activation_function_hidden(libfann.SIGMOID_SYMMETRIC)

ann.create_standard_array([2,2,1])

tr_data = libfann.training_data()
tr_data.set_train_data([[1,0],[0,1],[1,1],[0,0]],[[1],[1],[0],[0]]) 

ann.train_on_data(tr_data,1,1,1,1)
ann.save("wdata_test.txt")



