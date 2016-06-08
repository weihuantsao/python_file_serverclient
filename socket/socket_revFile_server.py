import socket
import sys
import os
s = socket.socket()
s.bind(('',9999))
s.listen(10)
print 'listening 9999 port ...'

def readlines(sock, recv_buffer=4096, delim='\n'):
    buffer = ''
    data = True
    while data:
        data = sock.recv(recv_buffer)
        buffer += data

        while buffer.find(delim) != -1:
            line, buffer = buffer.split('\n', 1)
            yield line
    return 


while True:
    filename =''
    filebuffer =''
    while(True):    
        sc, address = s.accept()
        print 'rev from:'+ str(address)
        for line in readlines(sc):
            if line.split('\t')[0] == '<<file>>':
                filename  = line.split('\t')[1]
                continue
            elif line == '<<EOF>>':
                f = open('rev_'+filename,'wb') #open in binary
                f.write(filebuffer)
                f.close()
                filebuffer = ''
                os.system('python txt2kml.py rev_%s' % filename)
                break
            else :
                filebuffer +=  line + '\n'

    sc.close()    
    
s.close()
