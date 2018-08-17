#this script uses python's soap API to make calls to get rules for the filewalls in the firewall.txt files  



from SOAPpy import SOAPProxy
import ssl
import xlsxwriter  #module for creating excel spreadsheet 
import base64 #allows for docoding base64 text
import string
import time
import math


starttime = time.asctime( time.localtime(time.time()) )
print "Start time time :", starttime
workbook = xlsxwriter.Workbook('Firewall_metric.xlsx')
data=open("firewalls.txt","r"); #creates and opens the needed files 
device_file=open("fail_device.txt","w")
device_file_list=open("device.txt","w")
summary=open("summary.txt","w")
summary.write(str(starttime)+"\n")
starttime = time.time()
firewalls=data.readlines()
print firewalls
#opens the file

def Service_by_firewall(device):
#connects to the firewalls and gets the list of service that is running on the firewall
        bold = workbook.add_format({'bold': True}) #formating text 
        worksheet = workbook.add_worksheet("service "+device[:22])
        proxy = 'https://'+sHost+'/AFA/php/ws.php?wsdl'
        host_Dat='' #connection information 
        rule=[]
        rule_list=[]
        namespace = 'https://www.algosec.com/afa-ws'
        soapaction='https://www.algosec.com/afa-ws/GetEntityNameRequest'
        server = SOAPProxy(proxy, namespace,soapaction) 
        #print device
        service_infor=server.GetServicesDeviceRequest(SessionID=SessionID, DeviceID=device)
                #run the function to get the data
        service_infor=str(service_infor)
        replacement_list=[" ","'","]",'"',"}","[","\n"]
        for items in replacement_list:#cleans the data 
                        service_infor=service_infor.replace(items,"")
        service_infor=service_infor.replace(": <",",")
        service_infor=service_infor.replace("{",",")
        service_infor=service_infor.split(",")
        ctr=0
        for reports in service_infor:
                ctr2=0
                for reports in service_infor:
                        if ":" not in reports:
                                if "Types.structType" not in reports: 
                                        #print reports
                                        service_infor[service_infor.index(reports)-1]=service_infor[service_infor.index(reports)-1]+"|"+reports
                                        service_infor.pop(service_infor.index(reports))
                                        ctr-=1
                        ctr+=1
        for z in service_infor:
                #print z
                if "Types.structType" in z: #cleans data
                        rule_list.append(rule)
                        rule=[] 
                        #report.pop(report.index(z))
                else:
                        z=z.split(":")
                        rule.append(z)
        #printrule_list
        rule_list.append(rule)
        #rule_list.pop(0)
        ctr2=0

        for  rules in rule_list:
                try:
                        if "DeviceID" in rules[0]:
                                rule_list.pop(ctr2)#cleans data
                except IndexError:
                        rule_list.pop(ctr2)
                ctr2+=1 
        for rules in rule_list:
                #print rules             
                rule_list.pop(0)        
        for x in range(len(rule_list[0])):
                worksheet.write(0,x,rule_list[0][x][0],bold)
                #wries the data to a excek files
        for rules in rule_list:
                row=rule_list.index(rules)+1
                for item in rules:
                        colum=rules.index(item)
                        worksheet.write(row,colum,item[1])
        worksheet.autofilter("A1:B1") #adds a filter to the top row

def Service(device,service,service_list):
#connects to algosec and gets the sevices 
        proxy = 'https://'+sHost+'/AFA/php/ws.php?wsdl'
        host_Dat='' #connection data
        namespace = 'https://www.algosec.com/afa-ws'
        soapaction='https://www.algosec.com/afa-ws/GetEntityNameRequest'
        server = SOAPProxy(proxy, namespace,soapaction)
        service_Dat=""
        #printservice
        if "|" in service: #handles mutiple hostgroup
                service=service.split("|")
                for services in service:
                        if services in service_list:
                                service_group=service_list[services]
                        else:
                                service_group=server.GetServiceNameDeviceRequest(SessionID=SessionID, DeviceID=device, Name=services) #soap function to get service
                                service_group=str(service_group)#cleans data
                                service_group=service_group.replace(": <",",")
                                service_group=service_group.replace("{",",")
                                service_group=service_group.split(",")
                                ctr=0
                                for services in service_group:
                                        if "structType" in services or ">:" in service:
                                                service_group.pop(ctr)
                                                ctr-=1
                                        ctr+=1
                                #service_group='\n'.join(service_group)
                                #service_group=service_group.split(",")
                                ctr=0
                                for services in service_group:
                                        if "structType" in services or ">:" in services:
                                                service_group.pop(ctr)
                                                #printservice_group
                                                ctr-=1
                                        ctr+=1
                                service_group='\n'.join(service_group)
                                replacement_list=[" ","'","]",'"',"{","}","["]
                                for items in replacement_list:
                                        service_group=service_group.replace(items,"")
                        service_Dat=service_Dat+"\n"+"\n"+service_group
                service_infor=service_Dat
                service_infor=service_infor[2:]
        else: 
                if service in service_list:
                        service_infor=service_list[service]
                else:
                        service_infor=server.GetServiceNameDeviceRequest(SessionID=SessionID, DeviceID=device, Name=service)
                        service_infor=str(service_infor)
                        service_infor=service_infor.replace(": <",",")
                        service_infor=service_infor.replace("{",",")#cleans data
                        service_infor=service_infor.split(",")
                        ctr=0
                        for services in service_infor:
                                if "structType" in services or ":" not in services:
                                        service_infor.pop(service_infor.index(services))
                                        service_infor.pop(ctr)
                                        ctr-=1
                                ctr+=1
                        ctr=0
                        for services in service_infor:
                                if "structType" in services or ">:" in service:
                                        service_infor.pop(ctr)
                                        #print service_infor
                                        ctr-=1
                                ctr+=1
                        service_infor='\n'.join(service_infor)
                        replacement_list=[" ","'","]",'"',"{","}","["]
                        for items in replacement_list:
                                service_infor=service_infor.replace(items,"")
                        service_infor=service_infor+"\n"
        return service_infor
def Hostgroup(device,hostgroup,host_list): 
#get information on the Host group 
        proxy = 'https://'+sHost+'/AFA/php/ws.php?wsdl'
        host_Dat=''
        namespace = 'https://www.algosec.com/afa-ws'
        soapaction='https://www.algosec.com/afa-ws/GetEntityNameRequest'
        server = SOAPProxy(proxy, namespace,soapaction)
        if "|" in hostgroup: #handles mutiple hostgroup
                hostgroup=hostgroup.split("|")
                #print hostgroup
                for hosts in hostgroup:
                        if hosts in host_list:
                                host=host_list[hosts]
                        else:
                                host=server.GetHostGroupNameDeviceRequest(SessionID=SessionID,DeviceID=device,HostGroupName=hosts) #soap function to get hostgroup
                                #sends the request to get host
                                host=str(host)
                                host=host.split('>:')
                                host.pop(0)
                                host=host[0]
                                replacement_list=[" ","'","]",'"',"{","}"]
                                for items in replacement_list:
                                        host=host.replace(items,"")
                        #print host
                                host=host.split(",")
                                ctr=0
                                host=str(host[:])
                                host=host.replace(']',"") #cleans data
                                host=host.replace('[',"")
                                host=host.replace("'","")
                                host=host.split(",")
                                host='\n'.join(host)
                        host_Dat=host_Dat+"\n"+"\n"+host
                host_Dat=host_Dat[2:]
                host=host_Dat
        else:
                if hostgroup in host_list:
                        host=host_list[hostgroup]
                else:
                        host=server.GetHostGroupNameDeviceRequest(SessionID=SessionID,DeviceID=device,HostGroupName=hostgroup)
                        #sends the request to get host
                        host=str(host)
                        host=host.split('>:')
                        host.pop(0)
                        host=host[0]
                        replacement_list=[" ","'","]",'"',"{","}"]
                        for items in replacement_list:
                                host=host.replace(items,"")
                        #print host
                        host=host.split(",")
                        host=str(host[:])
                        host=host.replace(']',"")
                        host=host.replace('[',"") #cleans the data 
                        host=host.replace("'","")
                        host=host.replace(" ","")
                        host=host.split(",")
                        host='\n'.join(host)
                        ctr=0
        return host
        
def exceldoc(filename):
#this funcation creates a excel document 
        sheet=open(filename+".csv","r")
        rules=sheet.readlines()
        host_list={}
        service_list={}
        bold = workbook.add_format({'bold': True}) # bolds the top line
        ctr=0
        for rule in rules:
                rules[ctr]=rule.split(",") # formats data
                ctr=ctr+1       
        #printfilename+".csv"
        lenght=len(rules[0])
        cell=string.ascii_uppercase[lenght-2]
        cell_end_letter='A1:'+cell+'1'
        try:
                device_name=rules[0].index("DeviceID")
                Destination=rules[0].index("Destination")
                service=rules[0].index("Service")
                Source=rules[0].index("Source")
        except:
                device_name=10
        worksheet = workbook.add_worksheet(rules[1][device_name][0:30]) #creates a new worksheet
        for rule in rules:
                row=rules.index(rule)
                for item in rule:
                        colum=rule.index(item)
                        if row==0:
                                host=worksheet.write(row, colum,item,bold)
                        else:
                                
                                if colum==Destination or colum==Source:
                                        worksheet.write(row, colum,item)
                                        try:
                                                host=Hostgroup(rules[1][device_name],item,host_list)
                                                host_list[item]=host
                                                if ":" in host :
                                                        hight=service_data.count("\n")
                                                        hight=hight*20
                                                        worksheet.write_comment(row,colum, host,{'height': hight, 'width': 200})
                                        except:
                                                pass
                                elif colum==service:
                                        worksheet.write(row, colum,item)
                                        service_data=Service(rules[1][device_name],item,service_list)
                                        service_list[item]=service_data
                                        hight=service_data.count("\n")
                                        hight=hight*17
                                        worksheet.write_comment(row,colum, service_data,{'height': hight})
                                else:
                                        worksheet.write(row, colum,item)
        worksheet.autofilter(cell_end_letter) #adds a filter to the top row
        Service_by_firewall(filename)
        
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
#returns a list of firewalls optional 
        SessionID = params['SessionID']
        device_list=[]
        device_infor=[]#connection information
        proxy = 'https://'+sHost+'/AFA/php/ws.php?wsdl'
        namespace = 'https://www.algosec.com/afa-ws'
        server = SOAPProxy(proxy, namespace)
        devices=server.GetDevicesListRequest(SessionID=SessionID)
        devices=str(devices)
        devices=devices.split(',')
        for device in devices:
                device_par=device.split(">:")
                if "Types.structType" in device_par[0] or "at" in device_par[0]:
                        device_par.pop(0)
                        try:
                                device_par=device_par[0]
                                replacement_list=[" ","'","]",'"',"{","}"]
                                for items in replacement_list:
                                        device_par=device_par.replace(items,"")
                                device_par=device_par.split(":")
                                #print device_par
                                device_file_list.write(device_par[0]+":"+device_par[1]+"n")
                                if "Policy" in device_par[0]:
                                        device_list.append(device_par[1])
                        except IndexError:
                                pass
                else:
                        try:
                                device_par=device_par[0]
                                replacement_list=[" ","'","]",'"',"{","}"]
                                for items in replacement_list:
                                        device_par=device_par.replace(items,"")
                                device_par=device_par.split(":")
                                #printdevice_par
                                device_file_list.write(device_par[0]+":"+device_par[1]+"\n")
                                if "ID" in device_par[0]:
                                        device_list.append(device_infor)
                                        device_infor=[]
                                        device_infor.append(device_par[0])
                                else:
                                        device_infor.append(device_par[0])
                        except:
                                pass
        #printdevice_list
        return device_list
                

        
def DisconnectAFA(params):
        # deconnects from algosec
        SessionID = params['SessionID']
        proxy = 'https://'+sHost+'/AFA/php/ws.php?wsdl'
        namespace = 'https://www.algosec.com/afa-ws'
        server = SOAPProxy(proxy, namespace)
        response = server.DisconnectRequest(SessionID=SessionID)
        return response
                
def SendQueryRequest(params,firewall):
                # Query the algosec server for information 
        firewall=firewall.replace("\n","")
        filename=firewall
        f=open(firewall+".csv","w")
        rule_list=[]
        rule=[]
        run="1" #check if the header was created 
        writelist=""
        namelist=""
        namelist="groupname," #varable to store the headers
        #print params
        SessionID = params['SessionID']
        #QueryInput = params['QueryInput']
        proxy = 'https://'+sHost+'/AFA/php/ws.php?wsdl'
        namespace = 'https://www.algosec.com/afa-ws' #connection information
        soapaction='https://www.algosec.com/afa-ws/GetEntityNameRequest'
        server = SOAPProxy(proxy, namespace,soapaction)
        report=server.GetRulesByDeviceRequest(SessionID=SessionID,DeviceID=firewall)
        report=str(report)
        print report 
        replacement_list=[" ","'","]",'"',"<u>","}"]
        for items in replacement_list:
                report=report.replace(items,"")
        report=report.replace("</u>"," ") #cleans up the data
        report=report.split("{")
        report.pop(0) 
        report_combine=""
        
        for reports in report:
                report_combine=report_combine+reports
        report=report_combine
        report=report.replace(">:",",")
        report=report.split(",")
        ctr=0
        for reports in report:
                ctr2=0          
                for reports in report:
                        if ":" not in reports:
                                 if "Types.structType" not in reports: 
                                        #print reports
                                        report[report.index(reports)-1]=report[report.index(reports)-1]+"|"+reports
                                        report.pop(report.index(reports))
                                        ctr-=1
                        ctr+=1
                        #removes uneeded data
        for z in report:
                #print z
                if "Types.structType" in z:
                        rule_list.append(rule)
                        rule=[] 
                        #report.pop(report.index(z))
                else:
                        z=z.split(":")
                        rule.append(z)
        #print rule_list
        rule_list.append(rule)
        rule_list.pop(0)
        for rule in rule_list:
                #changes the data into cvs format
                namelist=''
                for item in rule:
                        try:
                                writelist=writelist+str(item[0])+","
                                namelist=namelist+str(item[1])+","
                        except:
                                pass
                if run=="1":
                        #print writelist
                        f.write(writelist+"\n")
                        run="0"
                f.write(namelist+"\n")
        f.close()
        exceldoc(filename)

        return report
sHost = ''
print "\n" + "Submitting connect request:" + "\n"
pas=''
uname=''#login information 
values = {'UserName': uname, 'Password':pas , 'Domain': ''}
ssl._create_default_https_context = ssl._create_unverified_context
#stops ssl errors
afa_connect = ConnectAFA(values)
#runs the command to connect to algosec
global SessionID
SessionID = afa_connect
print "Returned Session ID: "+repr(SessionID)
QueryParams = {'SessionID': SessionID}

Devicelist(QueryParams)

for firewall in firewalls:
        print "\n" + "Submitting query request for:"+firewall+"\n"
        try:
                QueryResult = SendQueryRequest(QueryParams,firewall)
        except:
                device_file.write(str(firewall)+",")
print "\n" + "Submitting disconnect request:" + "\n"
DisconnectParams = {'SessionID': SessionID}
DisconnectResult = DisconnectAFA(DisconnectParams)
workbook.close()
device_file.close() #close the open files 
device_file_list.close()
print DisconnectResult
endtime = time.asctime( time.localtime(time.time()) )
summary.write(str(endtime)+"\n")
print "End time time :", endtime
endtime=time.time()#time information 
diff_time=endtime-starttime
print diff_time
hour=0
minutes=0
second=0
if diff_time > 60:
        diff_time=diff_time/60
        second, minutes=math.modf(diff_time)
        minutes=minutes*1
        second=second*60
        if minutes > 60:
                #print minutes
                hour=minutes/60
                minutes, hour=math.modf(hour)
                #print hour
                minutes=minutes*60
else:
        second=diff_time
print "It took "+str(hour)+" hours "+str(minutes)+" minutes "+str(second)+" seconds "
summary.write("It took "+str(hour)+" hours "+str(minutes)+" minutes "+str(second)+" seconds ")
summary.close
