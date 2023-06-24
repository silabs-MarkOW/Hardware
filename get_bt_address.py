import os
import sys

cmd = 'commander device info '+' '.join(sys.argv[1:])
fh = os.popen(cmd)
text = fh.read()
fh.close()

lines = text.split('\n')
for line in lines :
    if '' == line : continue
    tokens = line.split(':')
    if 'ERROR' == tokens[0] or 'WARNING' == tokens[0] :
        print(text)
        quit()
    if 'Unique ID' == tokens[0].strip() :
        euid64 = tokens[1].strip()
octets = []
for i in range(8) :
    if i < 3 or i > 4 :
        octets.append(euid64[2*i:][:2])
print(':'.join(octets))    
