#this script connects to algosec using algosec's soap ai to
#get tickets and write it to excel files


import ssl #SSL Support
import re #Regular Expressions
import base64
import datetime #Date and Time
import xlsxwriter
from algosec.api_client import FireFlowAPIClient
from suds.client import Client

def file():
# opens the file with all of the rules and the user's id  
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
        username="" #login information 
        password=""
        Request_id=Id[0]
        print Id
        client = FireFlowAPIClient(ip, username, password, verify_ssl=False)
        try:  #gets an ID and uses it to get a change request from algosec
                change_request = client.get_change_request_by_id(Request_id)
                change_request=Client.dict(change_request)
                return change_request
        except: # error for missing or invalid ID'S
                print "ID was not found "+Request_id
                return 1



workbook =xlsxwriter.Workbook('ticket_metric.xlsx')#manage excel file  
worksheet = workbook.add_worksheet("tickets")
split_information=file()
header={}
row=1#creates varables 
head_num=0
metric_list=[]
fail_request=[]  #create varable for later
file()
print split_information
request_list=[]
for Id in split_information:
        if Id != "id":
                change_request=login(Id)
                if change_request != 1:
                       try: 
                               test=change_request['trafficLines']
                               traffic=Client.dict(test[0]) #changes the traffic data into dictionary format
                               del change_request['trafficLines']
                               change_request.update(traffic)
                       except:
                               pass
                       metric_list.append(change_request)
for metric in metric_list:
        key=metric.keys()
        metric=dict(metric) #converts the varable to a dictionary
        for keys in key:
                if header.has_key(keys):
                        worksheet.write(row, header[keys],str(metric[keys]))
                else:                   #writes the data to a text file 
                        worksheet.write(0, head_num,keys)
                        print metric[keys]
                        worksheet.write (row, head_num,str(metric[keys]))
                        header[keys]=head_num
                        head_num+=1
        row=row+1

        
                        
                
workbook.close()

