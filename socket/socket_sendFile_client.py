import socket
import sys
import os

if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    print 'no parameter(filename)'
    quit()


s = socket.socket()
s.connect(("106.186.28.45",9999))

try: 
    if os.path.exists(filename) :
        s.send("\n<<file>>\t" + filename + "\n")
        s.send(open(filename,"rb").read()) #send file
        s.send("\n<<EOF>>\n") #send message indicating file transmission complete
    else:
        print ('no file')
	s.close()
except Exception,e:
	print str(e)
    #print 'No connection to the device could be established'
