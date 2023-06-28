import os

def get_dict(command,serial) :
    fh = os.popen('commander %s -s %s'%(command,serial))
    text = fh.read()
    fh.close()
    lines = text.split('\n')
    rd = {}
    for line in lines :
        if '' == line : continue
        tokens = line.split(':')
        if len(tokens) < 2 : continue
        if 'ERROR' == tokens[0] : return text
        if 'WARNING' == tokens[0] : return text
        key = tokens[0].strip()
        value = tokens[1].strip()
        cvalue = rd.get(key)
        if None == cvalue :
            rd[key] = value
        elif list == type(cvalue) :
            rd[key].append(value)
        else :
            rd[key] = [cvalue,value]
    return rd

def eui64_to_address(euid64) :
    octets = []
    for i in range(8) :
        if i < 3 or i > 4 :
            octets.append(euid64[2*i:][:2])
    return':'.join(octets)

PREFIX = 'usb-Silicon_Labs_J-Link'
files = os.listdir('/dev/serial/by-id')
output = [['Serial','Boards','VCOM','Device / Debug mode','SRAM','BT address']]
for file in files :
    if PREFIX != file[:len(PREFIX)] : continue
    left = file.index('_OB_')+4
    right = file.index('-if',left)
    serialNumber = file[left:right].lstrip('0')
    lineOutput = [serialNumber]
    boardInfo = get_dict('adapter probe',serialNumber)
    if dict != type(boardInfo) :
        print(boardInfo)
        quit()
    debugMode = boardInfo['Debug Mode']
    boards = boardInfo['Part Number']
    if list != type(boards) :
        boards = [boards]
    tl = []
    for b in boards :
        tl.append(b.split()[0][3:])
    lineOutput.append(','.join(tl))
    lineOutput.append(boardInfo['VCOM Port'])
    if 'MCU' == debugMode :
        deviceInfo = get_dict('device info',serialNumber)
        if dict != type(deviceInfo) :
            print(deviceInfo)
            quit()
        lineOutput.append(deviceInfo['Part Number'])
        lineOutput.append(deviceInfo['SRAM Size'])
        lineOutput.append(eui64_to_address(deviceInfo['Unique ID']))
    else :
        lineOutput.append(debugMode)
        lineOutput.append('')
        lineOutput.append('')
    output.append(lineOutput)

fmt = ''
for col in range(len(output[0])) :
    max = 0
    for row in range(len(output)) :
        l = len(output[row][col])
        if l > max : max = l
    fmt += '%%-%ds'%(max+1)

for row in range(len(output)) :
    c = ()
    for col in range(len(output[row])) :
        c += (output[row][col],)
    print(fmt%c)
