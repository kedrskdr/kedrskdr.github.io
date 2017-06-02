#!/usr/bin/env python
from fann2 import libfann
import re
import random
import sys

data = []
ext = []

for ss in  open("mod1_v.txt","r"):
	dat  = map(int,ss.strip().replace('\n', '').replace('\r', '').split(','))
	data.append(dat[:-1])
	ext.append(dat[-1:])

ann = libfann.neural_net()
ann.create_from_file("vir.txt")

for d in data:
	print ann.run(d)
