# -*- coding: utf-8 -*- 
import serial
import subprocess
import sys

if len(sys.argv) == 2:
    port = sys.argv[1]
else:
    print 'no parameter(serial port)'
    quit()

ser = serial.Serial()
ser.port = port
ser.baudrate = 115200


try:
    ser.open()
    while True:
        readline = lambda : iter(lambda:ser.read(1),"\n")
        line = "".join(readline())
        if line == "<<file>>":
            #second line is filename
            readline = lambda : iter(lambda:ser.read(1),"\n")
            filename = "".join(readline())
            path_file = ''
            
            if filename == 'apn':
                #path_file = 'C:/Users/Tsao/Desktop/' + filename
                path_file = '/etc/ppp/chatscripts/' + filename
            if filename == 'gateway.ini' or filename == 'rt3070.cfg' or filename == 'sim5320.cfg':
                #path_file = 'C:/Users/Tsao/Desktop/' + filename
                path_file = '/etc/gateway/' + filename
            if filename == 'wpa' or filename == 'wpa_supplicant.conf':
                #path_file = 'C:/Users/Tsao/Desktop/' + filename
                path_file = '/etc/' + filename
    
            with open(path_file,"wb") as outfile:
               while True:
                   line = "".join(readline())
                   if line == "<<EOF>>":
                       ser.write(path_file +' done\n')
                       
                       break #done so stop accumulating lines
                   print >> outfile,line
            
        if line == "<<config>>":
            #second line is protocol
            readline = lambda : iter(lambda:ser.read(1),"\n")
            cmd = "".join(readline())
            if cmd=='ping_test':
                ser.write('receiver on\n')
                print 'ping'
            elif cmd=='s51bgc_start':
                subprocess.call(["/etc/init.d/S51bgc", "start"])
                ser.write('s51bgc on\n')
                print 'recv s51bgc_on cmd'
            elif cmd=='s51bgc_stop':
                subprocess.call(["/etc/init.d/S51bgc", "stop"])
                ser.write('s51bgc off\n')
                print 'recv s51bgc_off cmd'
            elif cmd=='relay1on':
                subprocess.call(["/opt/app/gateway/scripts/rla", "-l","1"])
                ser.write('relay1 on\n')
                print 'recv relay1_on cmd'
            elif cmd=='relay1off':
                subprocess.call(["/opt/app/gateway/scripts/rla", "-l","0"])
                ser.write('relay1 off\n')
                print 'recv relay1_off cmd'
            elif cmd=='relay2on':
                subprocess.call(["/opt/app/gateway/scripts/rlb", "-l","1"])
                ser.write('relay2 on\n')
                print 'recv relay2_on cmd'
            elif cmd=='relay2off':
                subprocess.call(["/opt/app/gateway/scripts/rlb", "-l","0"])
                ser.write('relay2 off\n')
                print 'recv relay2_off cmd'                 
except :
    print 'No connection to the device could be established'