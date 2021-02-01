'''
written by: Lydia Unterreiner 1/25/2021
Copyright 2021 Reckon Point Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, 
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT 
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import serial
import time
import sys
from xml.dom import minidom

class config_bms():
    
    def __init__(self):
        # serial port
        self.port_name = '/dev/ttyS0'
        self.ser = ''
        
        # get & flag command for victron bms
        self.get_command = 8
        self.flag = '00'
        
        #create a dictionary to load xml parameters into
        self.config_dict = {}
          
    def initialize_port(self):
        try:
            self.ser = serial.Serial(self.port_name, 19200, timeout=10)
            print('Initialized port: ' + self.ser.name)
        except SerialException:
            print(self.port_name)
            sys.exit('Error: cannot open port, quitting...')

    def read_xml(self, xml_file):
        # read xml file
        print("reading xml file")
        mydoc = minidom.parse(xml_file)
        items = mydoc.getElementsByTagName('item')
        
        # store xml elements in dict
        for elem in items:
            self.config_dict[elem.attributes['name'].value] = [elem.attributes['value'].value, elem.firstChild.data]
        
        # convert values from str to int
        # then convert to hex
        for i in self.config_dict.values():
            i[0] = str(i[0])
            i[1] = int(i[1])
            i[1] = hex(i[1])
             
            # take out '0x' value in str
            i[0] = i[0][2:]
            i[1] = i[1][2:]
            
            # range values must be 4 digits long
            while len(i[1]) < 4:
                    i[1] = '0' + i[1]
            
            # convert to little endian
            first_id = i[0][2:]
            second_id = i[0][:2]  
            first_range = i[1][2:]
            second_range = i[1][:2]

            i[0] = first_id + second_id
            i[1] = first_range + second_range
            
            # make sure letters are capitilized
            i[0] = i[0].upper()
            i[1] = i[1].upper()
        
        # calculate checksum value and store in dictionary
        print("Calcaluting checksums")
        for i in self.config_dict:
            self.config_dict[i].append(self.calculate_checksum(self.config_dict[i][0], self.config_dict[i][1]))
            

    def calculate_checksum(self, name_id, name_range):
        # little endian
        name_id1 = '0x' + name_id[:2]
        name_id2 = '0x' + name_id[2:]
        name_range1 = '0x' + name_range[:2]
        name_range2 = '0x' + name_range[2:]
        
        #calculate checksum
        # 0x55 is max checksum value for victron bms
        checksum = hex(0x55 - self.get_command - int(name_id1, 16) - int(name_id2, 16) - int(name_range1, 16) - int(name_range2, 16))
        checksum = int(checksum, 16)
        
        # convert to correct positive hex value if checksum < 0
        if checksum < 0:
            checksum = hex(checksum & (2**32-1))
        else:
            checksum = hex(checksum)
        
        # format it correctly to parse later
        checksum = str(checksum)
        checksum = checksum[2:]
        
        if checksum[-1:] is 'L':
            checksum = checksum[-3:-1]
        else:
            checksum = checksum[-2:]
        
        # make sure checksum is length = 2
        if len(checksum) == 1:
            checksum  = '0' + checksum
            
        checksum = checksum.upper()
        
        return checksum
      
    def Victron_HEX_call(self):
        expected_read = ':'
        print("writing hex to victron bms \n")
        
        for i in self.config_dict:
            hex_to_write = ':' + str(self.get_command) + self.config_dict[i][0] + self.flag + self.config_dict[i][1] + self.config_dict[i][2]  + '\n'
            print('Setting: ' + i.upper() + ' \nhex sent: ' + hex_to_write)
            timeout = time.time() + 3 #s of timeout
            while True:
                self.ser.write(hex_to_write)                       # write hex to bms
                read_hex = self.ser.read_until(hex_to_write)       # Reading until hex_to_write is found

                if read_hex.find(hex_to_write[:-1]) != -1:   #Exiting after receiving a correct answer
                    print('Configuration complete, received HEX string: ' + read_hex[-1 * len(hex_to_write):])
                    print('*********************\n \n')
                    break 
                       
                elif time.time() > timeout:
                    #print('incorrect: ' + read_hex)
                    print('Timeout reached, check configuration and manually set')
                    break

            
if __name__ == "__main__":

    if (len(sys.argv) < 2):
        print("ERROR: missing parameter")
        print("example: python batter_monitor.py file_name.xml")
    else:
        config = config_bms()
        config.initialize_port()
        config.read_xml(sys.argv[1])
        config.Victron_HEX_call()
        





'''
}

ser = serial.Serial(
        port='/dev/ttyS0', # 
        baudrate = 19200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
) 

while 1:
    x=ser.readline()
    print(x)'''
'''

msg = "x"
ser.write(msg)
rsp =ser.readline()
print (rsp)'''
