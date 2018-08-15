#! /usr/bin/python
# This script connects to server over SSH to run commands to get port spanning information 
# the input is a text file called switch_list.txt that contain the ip address of the switches seperated with a new line   

import paramiko
import xlsxwriter
import socket  #import needed module
import time

def connection(IP_address):
#this function start the connection to the switch and login 
#and run commands to collect data 
	username = ""  #login information
	password = ""
	data_int=""
	ssh=paramiko.SSHClient()
	IP_address=IP_address.replace("\n","")
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	print IP_address
	try:
		ssh.connect(IP_address, username=username,password=password) #starts the connected
		shell=ssh.invoke_shell() #start a shell that allows for more than one command to be enter in one session 
		shell.send("enable\n")
		time.sleep(1)
		shell.send("") #enable password 
		time.sleep(1)
		shell.send("terminal length 0\n") #commands that are run on the switch 
		time.sleep(1)
		shell.send("show cdp neigh | exclude -w|,|AIR\n")
		time.sleep(1)
		data=shell.recv(9999)
		shell.send("show run | include interface|portfast\n")
		time.sleep(3)
		data_int=shell.recv(9999)
		ssh.close()
	except paramiko.AuthenticationException:
		data="AuthenticationException"
	except paramiko.ssh_exception.NoValidConnectionsError: #collection of error handling 
		data="NoValidConnectionsError"
	except paramiko.ssh_exception.SSHException:
		data="Incompatible version (1.5 instead of 2.0)"
	except socket.error:
		data="A connection attempt failed because the connected party"
	return data,data_int

def data_parse(data):
#this function parses data to make it easier to write data
	data=data.split("\n")
	#print data[5:]
	data=data[5:]
	ctr=0
	#print "data end"
	for ctr,line in enumerate(data):
		if len(line) < 55:
			#print line
			line=line.replace("\n","")
			data[ctr]=line[:16]
		else:
			line=line+"\n"
			data[ctr]=line
			
	data="".join(data)
	#print data 
	if len(data[0])> 1:
		resp="|".join(data)
		#print "resp is"
		#print resp
		resp=resp.split("|")
		for interface in resp:
			components = [interface[:10],interface[10:35],interface[35:41],interface[42:53],interface[53:60],interface[60:70],interface[70:]]
			##print components
			interface_split=interface.split(",")
			interface_split=filter(None,interface_split)
			for data in components:
				data_clean=data.replace(" ","")
				data_clean=data_clean.replace("\r\n","")
				data_clean=str(data_clean)
				if data_clean== u'':
					data_clean=""
				components[components.index(data)]=data_clean
			resp[resp.index(interface)]=components
		resp=filter(None,resp)
		##print resp
	else:
		resp=data.split("\n")

		for interface in resp:
			components = [interface[:17],interface[17:33],interface[33:45],interface[45:57],interface[57:]]
			#print components
			interface_split=interface.split(",")
			interface_split=filter(None,interface_split)
			for data in components:
				data_clean=data.replace(" ","")
				data_clean=data_clean.replace("\r\n","")
				data_clean=str(data_clean)
				if data_clean== u'':
					data_clean=""
				components[components.index(data)]=data_clean
			resp[resp.index(interface)]=components

	return resp

def data_parse_show(data):
#this funcation also parse the data data
	data=data.split("\n")
	data=data[1:]
	ctr=0
	#print "data end"
	for ctr,line in enumerate(data):
		
		if "interface" in line:
			try:
				if "spanning" in data[ctr+1]:
					#print line
					line=line.replace("\n","")
					data[ctr]=line
				else:
					line=line+"\n"
					data[ctr]=line
			except IndexError:
				line=line+"\n"
				data[ctr]=line   
		else:
			line=line+"\n"
			data[ctr]=line
			
	data="".join(data)
	#print data
	if len(data[0])> 1:
		resp="|".join(data)
		#print "resp is"
		#print resp
		resp=resp.split("|")
		for interface in resp:
			components =interface.split(" ")
			components =[" ".join(components[:2])," ".join(components[2:])]
			##print components
			interface_split=interface.split(",")
			interface_split=filter(None,interface_split)
			for data in components:
				data_clean=data.replace(" ","")
				data_clean=data_clean.replace("\r\n","")
				data_clean=str(data_clean)
				if data_clean== u'':
					data_clean=""
				components[components.index(data)]=data_clean
			resp[resp.index(interface)]=components
		resp=filter(None,resp)
		##print resp
	else:
		resp=data.split("\n")

		for interface in resp:
			print interface
			components =interface.split(" ")
			
			components =[" ".join(components[:2])," ".join(components[2:])]
			#print components
			interface_split=interface.split(",")
			interface_split=filter(None,interface_split)
			for data in components:
				data_clean=data.replace(" ","")
				data_clean=data_clean.replace("\r\n","")#cleans data
				data_clean=str(data_clean)
				if data_clean== u'':
					data_clean=""
				components[components.index(data)]=data_clean
			resp[resp.index(interface)]=components

	return resp

def excel(resp,ip_address):
	bold = workbook.add_format({"bold":True})
	try:
		host_name=socket.gethostbyaddr(ip_address)
		host_name=host_name[0]
	except:
		host_name=ip_address
	worksheet = workbook.add_worksheet(host_name[:30])
	#print resp
	
	for interfaces in resp:
		row=resp.index(interfaces)
		for items in interfaces:
			colum=interfaces.index(items)
			if row==0:
				worksheet.write(row, colum,items,bold)
			else:
				worksheet.write(row, colum, items)

def summary(resp,ip_address,row_global,summary_sheet):
#creates and writes the data into a excel sheet 
#
	bold = workbook.add_format({"bold":True})
	main=workbook.add_format({"bold":True})
	main.set_bg_color("#3366cc") #creates formating varables 
	side=workbook.add_format()
	side.set_bg_color("#d6e0f5")#background color
	try:#tries to covert to ip address into a hostname
		host_name=socket.gethostbyaddr(ip_address)
		host_name=host_name[0]
	except:
		host_name="not found"
	resp=resp
	#print resp
	
	for interfaces in resp:
		for items in interfaces:
			colum=interfaces.index(items)
			
			if row_global==0:#writes the header
				summary_sheet.write(row_global, colum,items,bold)
				summary_sheet.set_row(row_global,None,None,{'level':1, 'hidden': True})
			else:#writes the body data 
				summary_sheet.write(row_global, colum, items,side)
				summary_sheet.set_row(row_global,None,None,{'level':1, 'hidden': True})
		row_global+=1
		#writes the main body of the grouped data
	summary_sheet.write(row_global, 0, host_name,main)
	summary_sheet.write(row_global, 1, ip_address,main)
	summary_sheet.write(row_global, 2, "show cdp neigh | exclude -w|,|AIR",main)
	row_global+=1
	return row_global

def summary_show(resp,ip_address,row_global,summary_sheet):
#write data from the show run | include interface|portfast command into spreadsheet     
	print "summary_show"
	bdu_location=0
	bold = workbook.add_format({"bold":True})
	main=workbook.add_format({"bold":True})
	main.set_bg_color("#3366cc") #formating varable
	side=workbook.add_format()
	side.set_bg_color("#d6e0f5")

	try:#does a nslookup on the ipaddress
		host_name=socket.gethostbyaddr(ip_address)
		host_name=host_name[0]
	except:
		host_name="not found"
	resp=resp
	#print resp
	for interfaces in resp:
		for items in interfaces:#wries the data
			colum=interfaces.index(items)
			if "spanning-treeportfast" in items and colum==0:
				bdu_location=row_global
			if row_global==0:
				summary_sheet.write(row_global, colum,items,bold)
				summary_sheet.set_row(row_global,None,None,{'level':1, 'hidden': True})
			else:
				summary_sheet.write(row_global, colum, items,side)
				summary_sheet.set_row(row_global,None,None,{'level':1, 'hidden': True})
		row_global+=1
	summary_sheet.write(row_global, 0, host_name,main)
	summary_sheet.write(row_global, 1, ip_address,main)
	summary_sheet.write(row_global, 2, "show run | include interface|portfast",main)
	find='=IF(FIND("spanning",A'+str(bdu_location+1)+')=1,"good","bad")'
	print find
	summary_sheet.write(row_global, 3, find,main)
	row_global+=1
	return row_global


	    
workbook=xlsxwriter.Workbook("bdu_information.xlsx")#output excel file
file=open("switch_list.txt","r") #input files of switch ip seprated by a new line 

IP_address_list=file.readlines() #reads data
row_global=0 #keeps out of rows that have been written 
summary_sheet = workbook.add_worksheet("Summary")
for IP_address in IP_address_list:
	try:
		global summary_sheet
		global row_global
		data,data_response=connection(IP_address)
		response=data_parse(data)  
		row_global=summary(response,IP_address,row_global,summary_sheet)
		response=data_parse_show(data_response)
		row_global=summary_show(response,IP_address,row_global,summary_sheet)
	except:
		pass
file.close
workbook.close()
