import os
import socket
import time

def get_dict(command,sn=None,ip=None) :
    if None != sn :
        fh = os.popen('commander %s -s %s'%(command,sn))
    else :
        fh = os.popen('commander %s --ip %s'%(command,ip))       
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

def get_local(debug=True) :
    serialNumbers = []
    fh = os.popen('commander adapter list','r')
    text = fh.read()
    fh.close()
    lines = text.split('\n')
    for line in lines :
        if len(line) < 14: continue
        if 'serialNumber: ' != line[:14] : continue
        serialNumbers.append(line[14:])
    return serialNumbers

def get_remote(debug=True) :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    packet  =b'Discover'
    packet += bytes(64-len(packet))
    s.bind(('',19020))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(packet,('<broadcast>',19020))
    s.setblocking(False)
    start = time.time()
    timeout = start + 1
    ips = []
    while time.time() < timeout :
        try :
            data,origin = s.recvfrom(1518)
            if 128 != len(data) : continue
            if b'Found' != data[:5] : continue
            if 19020 != origin[1] : continue
            ips.append(origin[0])
        except BlockingIOError :
            time.sleep(.00001)
    return ips

output = [['Serial','Boards','VCOM','Device / Debug mode','SRAM','BT address']]
boardInfos = {}
for serialNumber in get_local() :
    boardInfo = get_dict('adapter probe',sn=serialNumber)
    if dict != type(boardInfo) : continue
    boardInfos[serialNumber] = boardInfo

for ip in get_remote() :
    boardInfo = get_dict('adapter probe',ip=ip)
    if dict != type(boardInfo) : continue
    serialNumber = boardInfo['J-Link Serial']
    boardInfo['IP'] = ip
    boardInfos[serialNumber] = boardInfo

for serialNumber in boardInfos :
    lineOutput = [serialNumber]
    boardInfo = boardInfos[serialNumber]
    debugMode = boardInfo['Debug Mode']
    boards = boardInfo['Part Number']
    if list != type(boards) :
        boards = [boards]
    tl = []
    for b in boards :
        tl.append(b.split()[0][3:])
    lineOutput.append(','.join(tl))
    ip = boardInfo.get('IP')
    if None == ip :
        lineOutput.append(boardInfo['VCOM Port'])
    else :
        lineOutput.append(boardInfo['IP'])
    if 'MCU' == debugMode or 'TARGET' == debugMode :
        if None == ip :
            deviceInfo = get_dict('device info',sn=serialNumber)
        else:
            deviceInfo = get_dict('device info',ip=ip)
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
