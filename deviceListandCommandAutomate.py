import re
import pprint
import netmiko
from getpass import getpass

inputf = open('connected_devices.txt', 'r')
output = open('devicelist.txt', 'w')
#ip = re.compile('(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))')


def make_connection (ip, username, password):
     return netmiko.ConnectHandler(device_type=’PaloAltoPanosSSH’, ip=ip, username=username, password=password)


def get_ips (file_name):
     for line in open(devicelist.txt, ‘r’).readlines():
     line = get_ip(line)
     for ip in line:
          ips.append(ip)



def getConnectedDevices():

		#Make connection to device:
		ip = re.compile('(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))')

		#This function creates a connection to Panorama, retrieves all connected devices and stores them to a text file 
		#This enables the commands that a user inputs to be run across all devices simultaneously.  

		Initiating Connection to Panorama to retrieve Devices
		panorama = input("Input the Panorama IP address you would like to retrieve connected devices from:")
		username = input(“Username: “)
		password = getpass()
		output_file = open('devicelist.txt', 'w')

		net_connect = make_connection(ip, username, password)

		#Clearing all the old info out of the device list file
		to_doc_w(devicelist.txt, “”)

		#Run a command and set that to output
		output = net_connect.send_command("show devices connected")
		inputf = open('connected_devices.txt', 'r')

		#for each_word in output:
			#to_doc_a(connected_devices.txt, output)  
        deviceList = []
        line = inputf.readlines()
        deviceDict = {}
        for i in line:
                messyList = []
                if ip.search(i):
                        messyList = i.split()
                        del messyList[0]
                        del messyList[2]
                        devHostname = messyList[0]
                        IPaddress = messyList[1]
                        deviceList.append([devHostname, IPaddress,"Device Name", "IP Address", "Device Type", "Password"])


                        for devices in messyList:
                                output.write(devices+'\n')

        print("Writing Device List")
        return deviceList


def panFirewallMultiConnect():
		#This code enables users to connect to account 
		#Prompt user for account info
		username = input(“Username: “)
		password = getpass()
		file_name = “userIDresults.csv”

		#For loop to hit all the devices. 
		for ip in ips:
			#Connect to a device
     		net_connect = make_connection(ip, username, password)

     		interface_list = []
      		for each_interface in output.split(” “):
     			if “ethernet” in each_interface:
     				iname = each_interface
     		interface_list.append(iname)

     		userid_list = []
     		second_command = net_connect.send_command_expect('show interface' + iname)
     		for each_useridenable in output.split(” “):
     			if 'userid-service:' in each_useridenable:
				enabled = each_useridenable
			userid_list.append(enabled)

			results = userid_list

			#results_dict = interface_list|userid_list TO BE COMPLETED LATER
			#(List composition function. Key is ifacename; yes or no is value)

			to_doc_a(file_name, results)

			#Ask user if they would like to display
			print("Results written to userIDresults.csv. Would you like to view the results from the console?")


def main():
        createDictionary(lineMatch())

main()
