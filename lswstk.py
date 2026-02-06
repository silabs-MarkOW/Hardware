import os
import socket
import time
import threading

#def get_dict(command,sn=None,ip=None,retries=1) :
def get_dict(command,genre,id,retries=1) :
    for attempt in range(retries) :
        if 'serialnumber' == genre :
            fh = os.popen('commander %s -s %s'%(command,id))
        elif 'ip' == genre :
            fh = os.popen('commander %s --ip %s'%(command,id))
        else :
            raise RuntimeError(genre)
        text = fh.read()
        fh.close()
        if text.find('ERROR: Could not connect debugger') < 0 : break
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
        if 'serialNumber: ' == line[:14] :
            serialNumbers.append(line[14:])
        elif '  serialNumber=' == line[:15] :
            serialNumbers.append(line[15:])
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

def worker(genre,id) :
    boardInfo = get_dict('adapter probe',genre,id)
    if dict != type(boardInfo) : return
    serialNumber = boardInfo['J-Link Serial']
    if 'ip' == genre :
        boardInfo['IP'] = id
    debugMode = boardInfo['Debug Mode']
    if 'MCU' == debugMode or 'TARGET' == debugMode :
        deviceInfo = get_dict('device info',genre,id,retries=3)
        boardInfo['deviceInfo'] = deviceInfo
        partno = deviceInfo.get('Part Number')
        if str != type(partno) or partno.find('917') < 0 :
            mfgInfo = None
        else :
            mfgInfo = get_dict('mfg917 info',genre,id,retries=3)
        boardInfo['mfgInfo'] = mfgInfo
    else :
        boardInfo['deviceInfo'] = None
    boardInfos[serialNumber] = boardInfo

threads = []
for serialNumber in get_local() :
    t = threading.Thread(target=worker,args=('serialnumber',serialNumber))
    threads.append(t)
    t.start()
    print('.',end='')
for ip in get_remote() :
    t = threading.Thread(target=worker,args=('ip',ip))
    threads.append(t)
    t.start()
    print('.',end='')
while True :
    print('\r',end='')
    live = 0
    for t in threads :
        if t.is_alive() :
            live += 1
            print('o',end='')
        else :
            print(' ',end='')
    if live == 0 :
        break
    time.sleep(0.01)
print('\r',end='')
    
for t in threads :
    t.join()
    
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
    deviceInfo = boardInfo['deviceInfo']
    mfgInfo = boardInfo.get('mfgInfo')
    if dict == type(deviceInfo) :
        if dict != type(deviceInfo) :
            print(deviceInfo)
            deviceInfo = {'Part Number':'','SRAM Size':'x x','Unique ID':''}
        part = deviceInfo['Part Number']
        isEFR32 = False
        if 'EFR32' == part[:5] or 'BGM' == part[:3] or 'MGM' == part[:3] :
            isEFR32 = True
            if 'EFR32' == part[:5] :
                part = part[5:]
        lineOutput.append(part)
        lineOutput.append(deviceInfo['SRAM Size'].split()[0])
        if isEFR32 :
            lineOutput.append(eui64_to_address(deviceInfo['Unique ID']))
        elif dict == type(mfgInfo) :
            bleAddr = mfgInfo.get('BLE MAC address')
            if str == type(bleAddr) :
                lineOutput.append(eui64_to_address(bleAddr[:6]+'0000'+bleAddr[6:]).lower())
            else :
                lineOutput.append('')
        else :
            lineOutput.append('')
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
