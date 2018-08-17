
from SOAPpy import SOAPProxy
import ssl
import xlsxwriter  #module for creating excel spreadsheet 
import base64 #allows for docoding base64 text
import string
import time
import math

def ConnectAFA(params):
#starts the connection to algosec 
	username = params['UserName']
	password = params['Password']
	domain = params['Domain']
	proxy = 'https://'+sHost+'/AFA/php/ws.php?wsdl'
	namespace = 'https://www.algosec.com/afa-ws'
	soapaction='https://www.algosec.com/afa-ws/GetEntityNameRequest'
	server = SOAPProxy(proxy, namespace,soapaction)
	response = server.ConnectRequest(UserName=username, Password=password, Domain=domain)
	return response

def Devicelist(params):
#returns a list of firewalls
	SessionID = params['SessionID']
	device_list=[]
	device_infor=[]
	proxy = 'https://'+sHost+'/AFA/php/ws.php?wsdl'
	namespace = 'https://www.algosec.com/afa-ws'
	server = SOAPProxy(proxy, namespace)
	devices=server.GetDevicesListRequest(SessionID=SessionID)#this makes the call to algosec  
	devices=str(devices)
	devices=devices.replace("-","_")#cleans the data
	devices=devices.split(',')
	for device in devices:
		if "structType" in device:
			device_list.append(device_infor)
			device_infor=[]
		else:
			replacement_list=["'","}","{"," "]#clean the data
			for x in replacement_list:
				device=device.replace(x,"")
			device=device.split(":")
			device_infor.append(device)

	print device_list
	return device_list
		
def matcher(device_list,device_name):
        device_id_list=[]
        #print device_list[1]
        for device in device_name:
                device=device.replace("-","_")
                device=device.replace("\n","")
                device=device.replace("#","")
                for data in device_list:
                        lenght=len(data)
                        if lenght==3:
                                try:
                                        #print device
                                        if device.lower() in data[1][1].lower():
                                                device_id_list.append(data[2][1])
                                except IndexError:
                                        pass
                                        #print data
                        if lenght==4:
                                if device.lower() in data[2][1].lower():
                                        device_id_list.append(data[3][1])
                                
        print device_id_list
        return device_id_list
                              
	
def DisconnectAFA(params):
	# deconnects from algosec
	SessionID = params['SessionID']
	proxy = 'https://'+sHost+'/AFA/php/ws.php?wsdl'
	namespace = 'https://www.algosec.com/afa-ws'
	server = SOAPProxy(proxy, namespace)
	response = server.DisconnectRequest(SessionID=SessionID)
	return response	

starttime = time.asctime( time.localtime(time.time()) )
print "Start time time :", starttime
starttime = time.time()
device_file=open("device_name.txt","r")
f=open("firewall.txt","w")
device_name=device_file.readlines()

sHost = ''
print "\n" + "Submitting connect request:" + "\n"
pas="" #password and username encoded
uname=""
values = {'UserName': uname, 'Password':pas , 'Domain': ''}
ssl._create_default_https_context = ssl._create_unverified_context
#stops ssl errors
afa_connect = ConnectAFA(values)
#runs the command to connect to algosec
global SessionID
SessionID = afa_connect
print "Returned Session ID: "+repr(SessionID)
QueryParams = {'SessionID': SessionID}

device_list=Devicelist(QueryParams)
device_id=matcher(device_list,device_name)
for device in device_id:
        f.write(str(device)+"\n")
print "\n" + "Submitting disconnect request:" + "\n"
DisconnectParams = {'SessionID': SessionID}
DisconnectResult = DisconnectAFA(DisconnectParams)
print DisconnectResult

                
