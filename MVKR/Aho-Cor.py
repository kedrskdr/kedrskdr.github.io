# -*- coding: utf-8 -*-
import sys
from cl_libr import *
from onemoreautomata import *
#read lines in file with sys calls
def helper(file):
	return (read_lines_in_file(file,[]))

def read_lines_in_file(file,mas):	
		
	for ss in open(file,"r"):
		dat = list(map(int,ss.strip().replace('\rn', '').split(',')))
		mas.append(dat)
	return (mas)
	

file = str("out.mg_test_ppt.txt")


#список с строками из файла
strr = helper(file)

patterns = [strr[87]] #goes down

#f =fsa()
#f.addpattern(patterns) 
#print ("len strings",len(patterns[0]),len(patterns[1]))	
#print("count",f.getnodecount())
#print("durch automat kommen und ein wort finden ob es gibt oder nicht",f.durchgehen(strr[4]))

a = onemoreSuffixAutomaton()
ed = a.SuffixAutomaton(strr[87])
print(len(ed))
