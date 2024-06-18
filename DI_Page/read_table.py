def get_tokens(line, expected) :
    tokens = line.split()
    if len(tokens) < expected :
        return tokens
    start = 0
    for i in range(4) :
        offset = line[start:].find(tokens[i])
        if offset < 0 :
            raise RuntimeError
        start += offset
        if i < 3 :
            start += len(tokens[i])
    return tokens[:3]+[line[start:]]
    
def get_offsets(text) :
    lines = text.strip().split('\n')
    got_header = False
    db = {}
    for line in lines :
        tokens = get_tokens(line, 4)
        if not got_header :
            if 'Offset' != tokens[0] or 'Name' != tokens[1] or 'Type' != tokens[2] :
                raise RuntimeError(tokens)
            got_header = True
            continue
        if '0x' != tokens[0][:2].lower() :
            raise RuntimeError(line)
        offset = int(tokens[0][2:],16)
        prev = db.get(tokens[1])
        if None != prev :
            raise RuntimeError('duplicate offset for %s: 0x%x and 0x%x'%(tokens[1],prev,offset))
        db[tokens[1]] = offset
    return db

def get_bits(text) :
    lines = text.strip().split('\n')
    db = {}
    register = None
    for line in lines :
        tokens = get_tokens(line, 4)
        if 1 == len(tokens) :
            register = tokens[0]
            db[register] = {}
            continue
        db[register][tokens[1]] = tokens[0]
    return db
