import serial   #Using pyserial Library
from serial import SerialException
import serial.tools.list_ports
import time     #for loop timeout
import serial.tools.list_ports
import sys      #for sys.exit in while True loop
import logging as log
log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


#Checking command line input arguments
if len(sys.argv) < 3:
	print repr("Please sepcify a USB port and command to send (without : and \n), example:")
	print "   sudo python hex_test.py /dev/ttyUSB0 7ECED0075"
	exit()




def initialize_port(port_name):
    try:
        ser = serial.Serial(port_name, 19200, timeout=10)
        log.debug('Port: %s', ser.name)
    except SerialException:
        print port_name
        sys.exit('Error: cannot open port, quitting...')
    return ser



def Victron_HEX_call(ser, write_hex, expected_read):
    log.info('Sending %s to %s', write_hex, ser.name)
    print(write_hex)

    timeout = time.time() + 3 #s of timeout
    while True:
        
        ser.write(write_hex)
  
        read_hex=ser.read_until('\n')       #Reading until "\n" symbol
        
        if read_hex[0:len(expected_read)] == expected_read:     #Exiting after receiving a correct answer
            log.info('Received HEX string: %s \n', read_hex)
            break
               
        elif time.time() > timeout:
            log.warning('Timeout reached, received HEX string: %s \n', read_hex)
            break
    
    return read_hex


 

#Initialize Serial Port
ser = initialize_port(sys.argv[1])

#Sending command
read_hex = Victron_HEX_call(ser, ':' + sys.argv[2] + '\n', ':')
ser.close()

print 'Received answer: ' + read_hex