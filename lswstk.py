import threading
import os
import time

def subprocess(fd_in,fd_out,fd_error,ip,lock) :
    print('subprocess(fd_in:%d,fd_out:%d,fd_error:%d,ip:"%s")'%(fd_in,fd_out,fd_error,ip))
    pid = os.fork()
    if pid < 0 :
        print('Fork failure %s'%(ip))
        lock.acquire()
        states[ip] = 3
        lock.release()
        return
    if 0 == pid :
        os.dup2(fd_in,0)
        os.close(fd_in)
        os.dup2(fd_out,1)
        os.close(fd_out)
        os.dup2(fd_error,2)
        os.close(fd_error)
        os.execvp("commander",["commander","adapter","probe","--ip",ip])
    else :
        (epid, status) = os.waitpid(pid, 0)
        if epid == pid :
            print('%s commander exited'%(ip),status)
            lock.acquire()
            if status :
                states[ip] = 3
            else :
                states[ip] = 2
            lock.release()
            return

def preader(fd,ip,lock) :
    global active
    print('reader(fd:%d,ip:"%s"): pid:%d'%(fd,ip,os.getpid()))
    text = b''
    os.set_blocking(fd,False)
    while True :
        lock.acquire()
        state = states[ip]
        if 2 == state :
            results[ip] = text
            states.pop(ip)
        if 3 == state :
            states.pop(ip)
        lock.release()
        if state > 1 :
            print('reader exiting ip:%s, state:%d'%(ip,state))
            return
        try :
            byte = os.read(fd,1)
            text += byte
        except :
            time.sleep(.01)
    
def process(ip,lock) :
    global states
    lock.acquire()
    states[ip] = 1
    lock.release()    
    print('process("%s")'%(ip))
    (read_in,write_in) = os.pipe()
    (read_out,write_out) = os.pipe()
    (read_error,write_error) = os.pipe()
    p = threading.Thread(target=subprocess,args=(read_in,write_out,write_error,ip,lock))
    r = threading.Thread(target=preader,args=(read_out,ip,lock))
    print('starting reader %s'%(ip))
    r.start()
    print('starting subprocess')
    p.start()
    p.join()
    print('process exiting')

states = {}
results = {}
lock = threading.Lock()
for a in range(15,60) :
    ip = "192.168.0.%d"%(a)
    p = threading.Thread(target=process,args=(ip,lock))
    lock.acquire()
    states[ip] = 0
    count = len(states)
    lock.release()
    p.start()
    if count > 15 :
        time.sleep(1)
    else :
        time.sleep(.1)

while True :
    lock.acquire()
    count = len(states)
    lock.release()
    if 0 == count :
        break
    time.sleep(1)

for ip in results :
    lines = results[ip].decode().split('\n')
    name = 'unknown'
    part = 'unknown'
    for line in lines :
        tokens = line.split()
        if 4 == len(tokens) \
           and 'J-Link' == tokens[0] \
           and 'Serial' == tokens[1] \
           and ':' == tokens[2] :
            serial = tokens[3]
        if len(tokens) > 2 \
           and 'Name' == tokens[0] \
           and ':' == tokens[1] :
            name = tokens[2]
        if len(tokens) > 3 \
           and 'Part' == tokens[0] \
           and 'Number' == tokens[1] \
           and ':' == tokens[2] :
            part = ' '.join(tokens[3:])
    print('%s %s %s %s'%(ip,serial,name,part))
    if 'unknown' == name :
        print(results[ip])
