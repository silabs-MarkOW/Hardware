import bincopy
import sys
import argparse
import tempfile
import os
import di_map

parser = argparse.ArgumentParser()
source = parser.add_mutually_exclusive_group(required=True)
source.add_argument('--usb')
source.add_argument('--ethernet')
source.add_argument('--file')
parser.add_argument('--map',required=True)
parser.add_argument('--register',required=True)
args = parser.parse_args()

map = di_map.DI_Map(args.map)
if None != args.usb :
    source = '-s %s'%(args.usb)
elif None != args.ethernet :
    source = '--ip %s'%(args.ethernet)
else :
    source = None
if None != source :
    fd,name = tempfile.mkstemp(suffix='.hex')
    command = 'commander readmem --region=@devinfo -o %s %s'%(name,source)
    os.system(command)
    os.close(fd)
    image = bincopy.BinFile(name)
    os.unlink(name)
else :
    image = bincopy.BinFile(args.file)

offset = map.offset[args.register]
reg = int.from_bytes(image[image.minimum_address+offset:][:4],'little')
print('%s: 0x%03x 0x%08x'%(args.register,offset,reg))
