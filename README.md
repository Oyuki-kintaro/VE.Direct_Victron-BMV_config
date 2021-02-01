# VE.Direct_Victron-BMV_config

Script developed on bmv-712 smart

****Please read hex protocol pdf****
\npdf file contains information on command flags and hex id's used when sending messages to the bmv

To run file open a terminal and enter "python config_battery_monitor.py bms.xml"

- bms.xml 
    This is a parameter file that config_batter_monitor.py reads in. Data from this file is stored in a dictionary for the configuration script to use when solving for the correct hex value to send to the bmv. You can edit this file by adding or removing parameters, just make sure the format remains the same
    
- config_battery_monitor.py
    This script reads in parameters from bms.xml file, retrieves the hex value equivalent of the range id, converts to little endian and solves for the correct checksum value. Then a string of all the values concatenated together in the acceptable format are sent. The response more often than not should match the hex value sent. 
    If timeout is reached, manually double check the monitor to verify setting. ID 0x034F or the Relay Mode will timeout unlike the others because its response comes without a flag so it is one of the few responses that will not match the hex value sent. 
    
    
    
- hex-test.py
    This script is not of my own development but helped me develope some of my code. A link of where the code was found is provided in the first lines commented out. Very helpful in veryfing hex values and understanding how communication to the bmv works.
    This is a seperate script to individually configure settings. enter "sudo python hex-test.py '/dev/ttyXX' hex-value" to use. Entering "451" as the hex-value in this instance should return the product id. in my case it was '181A330'.
    
    451 => 4 is the product id command; 51 is the checksum
    181A330 => 1 is the done/sucessful response; 81A3 is the hex id 0xA381 for bmv712; 30 is the checksum
    
