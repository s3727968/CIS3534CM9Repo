#!/usr/bin/env python3
#networkFileRW.py
#Fatima Bueno
#July 31, 2023
#Update routers and switches;
#read equipment from a file, write updates & errors to file

##---->>>> Use a try/except clause to import the JSON module
import json
try:
    routers = {"router1":"10.10.10.1", "router2":"20.20.20.1", "router3":"30.30.30.1"}

    filename_r = 'equip_r.json'
    with open(filename_r, 'w') as f:
        json.dump(routers, f)

    switches = {"switch1":"10.10.10.2", "switch2":"10.10.10.3", "switch3":"10.10.10.4",
                "switch4":"10.10.10.5", "switch5":"20.20.20.2", "switch6":"20.20.20.3",
                "switch7":"30.30.30.2", "switch8":"30.30.30.3", "switch9":"30.30.30.4"}
    filename_s = 'equip_s.json'
    with open(filename_s, 'w') as f:
        json.dump(switches, f)

except FileNotFoundError:
    print('Sorry file does not exist')
   
##---->>>> Create file constants for the file names; file constants can be reused
EQUIP_R = 'equip_r.txt'
EQUIP_S = 'equip_s.txt'
UPDATED_EQUIP = 'updated.txt'
INVAL_ADD = 'errors.txt'
##         There are 2 files to read this program: equip_r.txt and equip_s.txt
##         There are 2 files to write in this program: updated.txt and errors.txt
      




#prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

#function to get valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        #prompt for device to update
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device  
        else:
            print("That device is not in the network inventory.")

#function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        #print("octets", octets)
        for byte in octets:
            byte = int(byte)
            if byte < 0 or byte > 255:
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                print(SORRY)
                break
        else:
            #validIP = True
                return ipAddress, invalidIPCount
                #don't need to return invalidIPAddresses list - it's an object
        
def main():

    ##---->>>> open files here
    #dictionaries
    ##---->>>> read the routers and addresses into the router dictionary
    filename_r = 'equip_r.json'
    with open(filename_r) as f:
        routers = json.load(f)
        
##    routers = {}
    


    ##---->>>> read the switches and addresses into the switches dictionary
    filename_s = 'equip_s.json'
    with open(filename_s) as f:
        switches = json.load(f)

##    switches = {}


    #the updated dictionary holds the device name and new ip address
    updated = {}

    #list of bad addresses entered by the user
    invalidIPAddresses = []

    #accumulator variables
    devicesUpdatedCount = 0
    invalidIPCount = 0

    #flags and sentinels
    quitNow = False
    validIP = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items(): 
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:

        #function call to get valid device
        device = getValidDevice(routers, switches)
        
        if device == 'x':
            quitNow = True
            break
        
        #function call to get valid IP address
        #python lets you return two or more values at one time
        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)
  
        #update device
        if 'r' in device:
            #modify the value associated with the key
            routers[device] = ipAddress 
            #print("routers", routers)
            
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        #add the device and ipAddress to the dictionary
        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)
        #loop back to the beginning

    #user finished updating devices
    print("\nSummary:")
    print()
    print("Number of devices updated:", devicesUpdatedCount)

    ##---->>>> write the updated equipment dictionary to a file
    with open(UPDATED_EQUIP, 'w') as f:
        f.write(str(updated))
       
 
    print('Updated equipment written to file updated.txt')
    print()
    print('\nNumber of invalid addresses attempted: ', invalidIPCount)

    ##---->>>> write the list of invalid addresses to a file
    with open(INVAL_ADD, 'w') as f:
        f.write(str(invalidIPAddresses))
    print("List of invalid addresses written to file errors.txt")

#top-level scope check
if __name__ == "__main__":
    main()


