#this script connects to algosec's api to count the number of rules made in each request

import ssl #SSL Support
import re #Regular Expressions
import datetime #Date and Time
import base64
import urllib3
from algosec.api_client import FireFlowAPIClient
def file():
# opens the file with all of the rules adn the user's id  
	f=open("ticket.txt","r")
	combine_information=f.readlines()
	split_information=[]
	for line in combine_information:
		um_data=line.split("|")
		try:
			um_data[0]=um_data[0].replace(" ","")
			um_data[1]=um_data[1].replace(" ","") # removes the space and new line from data 
			um_data[1]=um_data[1].replace("\n","")
			split_information.append(um_data)
		except IndexError: # debug code 
			pass 
	#print split_information
	return (split_information)
def login(Id):
# this function logs into algosec and look for a user ID 
	ip=""
	username=
	password=
	Request_id=Id
	print Id
	client = FireFlowAPIClient(ip, username, password, verify_ssl=False)
	try:  #gets an ID and uses it to get a change request from algosec
		change_request = client.get_change_request_by_id(Request_id)
		return change_request
	except: # error for missing or invalid IDS
		print "ID was not found "+Request_id
		return "none"
	#print change_request[1] 
def counter(change_request):
	number=0
	for x in change_request:
			data=" ".join(str(y) for y in x) 
			data=data.replace("\n"," ")
			#print data
			#looks for the word trafficUser[] and prints out the number of times that i shows up
			if "trafficUser[]" in data:
				number=data.count("trafficUser[]")
				print "number of rules are: "
				print number
	return number
def eid(change_request): 
# this fuction finds the user's EID from the ticket information
	for x in change_request:
			data=" ".join(str(y) for y in x) 
			data=data.split("\n")
			for z in data:
				if "owner" in z:
					data=z
					return data
	 
split_information=file()
metric_list=[]
fail_request=[]  #create varable for later
total_number_rule=0
total_number_tickets=0 
metric_Data={"owner" :" ","number of request":1, "number of rule":0} # creates a dictionary to store data
metric_list.append(metric_Data)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
for Id in split_information:
	if "id"not in Id[0]:
		change_request=login(Id[0])
		print "change request number is: "
		print change_request
		if "none" not in change_request:
			number_of_rule=counter(change_request)
			total_number_rule=total_number_rule+number_of_rule #counts the number of rules
			owner=eid(change_request)
			owner=owner.split(" ")
			owner=owner[1]
			ctr=0
			inside_list="false" 
			for users in metric_list: #check to see of the user is in the list 
				if str(owner) in users.get("owner"):
					metric_Data={"owner" :owner,"number of request": users.get("number of request")+1, "number of rule": users.get("number of rule")+number_of_rule}
					metric_list[ctr]=metric_Data
					inside_list="true"
					total_number_tickets+=1
					break 
				ctr=ctr+1
			if  inside_list== "false": 
				metric_Data={"owner" :owner,"number of request":1, "number of rule":number_of_rule}
				print "metric data is: "
				print metric_Data
				metric_list.append(metric_Data)
				total_number_tickets+=1
			print total_number_tickets
		else:
			fail_request.append(Id[0])
fail_request_t2=[]
print "checking fail request"
for request in fail_request:
	request=request.replace(" ","")
	change_request=login(request)
	print "change request number is: "
	print change_request
	if "none" not in change_request:
		number_of_rule=counter(change_request)
		total_number_rule=total_number_rule+number_of_rule
		owner=eid(change_request)
		owner=owner.split(" ")
		owner=owner[1]
		ctr=0
		inside_list="false" 
		for users in metric_list:
			if str(owner) in users.get("owner"):
				metric_Data={"owner" :owner,"number of request": users.get("number of request")+1, "number of rule": users.get("number of rule")+number_of_rule}
				metric_list[ctr]=metric_Data
				inside_list="true"
				total_number_tickets+=1
				break 
			ctr=ctr+1
		if  inside_list== "false": 
			metric_Data={"owner" :owner,"number of request":1, "number of rule":number_of_rule}
			print "metric data is: "
			print metric_Data
			metric_list.append(metric_Data)
			total_number_tickets+=1
		print total_number_tickets
	else:
		fail_request_t2.append(change_request)
		
print metric_list
fw=open("metric.txt","w")
fw.write(str(datetime.datetime.now()))
fw.write("\n")
fw.write("total number of rules:")
fw.write(str(total_number_rule))
fw.write("\n")
fw.write("total number of tickets:")
fw.write(str(total_number_tickets))
fw.write("\n")
fw.write("owner,number of request,number of rules\n")
for data in metric_list:
	fw.write(data.get("owner"))
	fw.write(",")
	fw.write(str(data.get("number of request")))
	fw.write(",")	
	fw.write(str(data.get("number of rule")))
	fw.write("\n")	
