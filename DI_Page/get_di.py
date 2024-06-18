import argparse
import jumbo
import panther
import lynx
import bobcat
import margay
import bincopy

families = [jumbo,panther,lynx,bobcat,margay]

parser = argparse.ArgumentParser()
parser.add_argument('--image',help='image of Device Information page',required=True)
parser.add_argument('--register',help='Register to display')
parser.add_argument('--decimal',action='store_true',help='values in decimal')
parser.add_argument('--debug',action='store_true',help='additional info')
args = parser.parse_args()

def get_register(module,name) :
    if args.debug : print('get_register(module=%s,name=%s)'%(module.__str__(),name))
    soff = 0
    if jumbo == module :
        soff = 0x1b0
    offset = module.offsets.get(name)
    if None == offset :
        raise RuntimeError(name)
    if args.debug :
        print('%s offset: 0x%x'%(name,offset))
    return int.from_bytes(image[soff+offset:][:4],'little')
    
def get_bitfield(value,bits) :
    tokens = bits.split(':')
    if 1 == len(tokens) :
        return 1 & (value >> int(bits))
    left = int(tokens[0])
    right = int(tokens[1])
    mask = (1 << left) - 1
    return (value & mask) >> right

def render_bits(bits, value) :
    for key in bits :
        if args.decimal :
            format = '  %s: %d'
        else :
            format = '  %s: 0x%x'
        print(format%(key,get_bitfield(value,bits[key])))
        
image = bincopy.BinFile(args.image).as_binary()

for module in families :
    register = get_register(module,'PART')
    if args.debug :
        print('determining family: PART: %08x'%(register))
    bits = module.bits['PART'].get('DEVICE_FAMILY')
    if None == bits :
        bits = module.bits['PART'].get('FAMILY')
        
    family = get_bitfield(register,bits)
    if args.debug :
        print('family: %d'%(family))
    if module == jumbo and family > 27 and family < 40 :
        family = jumbo
        break
    if module == panther or module == lynx or module == bobcat or module == margay :
        bits = module.bits['PART'].get('FAMILYNUM')
        familynum = get_bitfield(register,bits)
        if 21 == familynum :
            family = panther
        elif 22 == familynum :
            family = lynx
        elif 24 == familynum :
            family = bobcat
        elif 28 == familynum :
            family = margay
        else :
            raise RuntimeError(familynum)
        break
if args.debug :
    print('Identified image as %s family'%(family.__name__))
            
if 'list' == args.register :
    print('Registers: %s'%(', '.join(list(family.offsets.keys()))))
    quit()

if None != args.register :
    register = get_register(family,args.register)
    bits = family.bits.get(args.register)
    if None != bits :
        render_bits(bits, register)
    else :
        print('%s: 0x%08x'%(args.register,register))
    quit()

for name in family.offsets :
    register = get_register(family,name)
    print('%s: 0x%08x'%(name,register))
    bits = family.bits.get(name)
    if None != bits :
        render_bits(bits, register)
    
