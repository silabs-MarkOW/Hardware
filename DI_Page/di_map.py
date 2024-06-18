import sys

class DI_Map :
    def __init__(self,filename) :
        fh = open(filename,'r')
        text = fh.read()
        fh.close()
        lines = text.split('\n')
        self.offset = {}
        lc = 0
        for line in lines :
            lc += 1
            if len(line) < 2 : continue
            if '0x' != line[:2]  : continue
            tokens = line.split()
            if len(tokens) < 2 :
                raise RuntimeError('Bad line %d (%s)'%(lc,line))
            offset = int(tokens[0][2:],16)
            self.offset[tokens[1]] = offset

if '__main__' == __name__ :
    maps = {}
    for family in sys.argv[1:] :
        maps[family] = DI_Map(family+'.txt')
        #print(maps[family].__dict__)

    names = {}
    offsets = {}
    for family in maps :
        print('processing %s'%(family))
        for name in maps[family].offset :
            offset = maps[family].offset[name]
            value = names.get(name)
            if None == value :
                names[name] = offset
            else :
                if value != offset :
                    print('Mismatch %s at 0x%x and 0x%x'%(name,offset,value))
            value = offsets.get(offset)
            if None == value :
                offsets[offset] = name
            else :
                if value != name :
                    print('Mismatch 0x%x contains %s and %s'%(offset,name,value))
