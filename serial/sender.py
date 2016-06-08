# -*- coding: utf-8 -*- 
import serial
import sys
import os
import ConfigParser

if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    print 'no parameter(filename)'
    quit()


def ConfigSectionMap(section):
    dict1 = {}
    options = Parser.options(section)
    for option in options:
        try:
            dict1[option] = Parser.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

Parser = ConfigParser.ConfigParser()
Parser.read('gateway.ini')
port = ConfigSectionMap("MANAGER")['sender_port']


s = serial.Serial()
s.port = port
s.baudrate = 115200
s.timeout = 2


try: 
    s.open()
    if filename == 'ping':
        s.write("\n<<config>>\n" + 'ping_test' + "\n")
        line = s.readline()
        print line
    elif filename == 'b_on':
        s.write("\n<<config>>\n" + 's51bgc_start' + "\n")
        line = s.readline()
        print line
    elif filename == 'b_off':
        s.write("\n<<config>>\n" + 's51bgc_stop' + "\n")
        line = s.readline()
    elif filename == 'r1_on':
        s.write("\n<<config>>\n" + 'relay1on' + "\n")
        line = s.readline()
        print line
    elif filename == 'r1_off':
        s.write("\n<<config>>\n" + 'relay1off' + "\n")
        line = s.readline()
        print line
    elif filename == 'r2_on':
        s.write("\n<<config>>\n" + 'relay2on' + "\n")
        line = s.readline()
        print line
    elif filename == 'r2_off':
        s.write("\n<<config>>\n" + 'relay2off' + "\n")
        line = s.readline()
        print line
    else:
        if os.path.exists(filename) :
            s.write("\n<<file>>\n" + filename + "\n")
            s.write(open(filename,"rb").read()) #send file
            s.write("\n<<EOF>>\n") #send message indicating file transmission complete
            line = s.readline()
            print line
        else:
            print ('no file')
    s.close()
except :
    print 'No connection to the device could be established'


