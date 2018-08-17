#! /usr/bin/python


import paramiko
import xlsxwriter #import module 
import socket

def connection(IP_address,maker):
#start a connect to the switch and runs the show ver command to get the module and show interfaces 
        username = ""
        password = ""
        fc=open("special_cisco.txt")
        special_cisco=fc.readlines()
        ssh=paramiko.SSHClient()
        #print maker
        IP_address=IP_address.replace("\n","")
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
                ssh.connect(IP_address, username=username,password=password)
                stdin,stdout,stderr=ssh.exec_command("show ver")
                maker=stdout.readlines()
                print maker
                if "isco" in maker:
                        if maker in special_cisco:
                                stdin,stdout,stderr=ssh.exec_command("show interfaces stat")
                        else:
                                stdin,stdout,stderr=ssh.exec_command("show interfaces status")
                if "uniper" in maker:
                        stdin,stdout,stderr=ssh.exec_command("show int Terse")
                if "rocade" in maker:
                        stdin,stdout,stderr=ssh.exec_command("show int bri")
                data=stdout.readlines()
                ssh.close()
        except paramiko.AuthenticationException:
                data="AuthenticationException"
        except paramiko.ssh_exception.NoValidConnectionsError:
                data="NoValidConnectionsError"
        except paramiko.ssh_exception.SSHException:
                data="Incompatible version (1.5 instead of 2.0)"
        except socket.error:
                data="A connection attempt failed because the connected party"
        return data

def data_pars(data):
        resp="|".join(data)
        resp=resp.split("|")
        for interface in resp:
                components = [interface[:17],interface[17:35],interface[35:49],interface[49:58],interface[58:]]
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
        resp=filter(None,resp)
        #print resp
        return resp
                
def excel(resp,ip_address):
        bold = workbook.add_format({"bold":True})
        try:
                host_name=socket.gethostbyaddr(ip_address)
                host_name=host_name[0]
        except:
                host_name=ip_address
        worksheet = workbook.add_worksheet(host_name[:30])
        print resp
        
        for interfaces in resp:
                row=resp.index(interfaces)
                for items in interfaces:
                        colum=interfaces.index(items)
                        if row==0:
                                worksheet.write(row, colum,items,bold)
                        else:
                                worksheet.write(row, colum, items)
                                                                
def summary(resp,ip_address,row_global,summary_sheet):
        bold = workbook.add_format({"bold":True})
        try:
                host_name=socket.gethostbyaddr(ip_address)
                host_name=host_name[0]
        except:
                host_name="not found"
        print resp
        
        for interfaces in resp:
                for items in interfaces:
                        colum=interfaces.index(items)
                        if row_global==0:
                                summary_sheet.write(row_global, colum,items,bold)
                        else:
                                summary_sheet.write(row_global, colum, items)
                row_global+=1
        return row_global
                
def chart():
        summary_sheet.write(1, 11, '=COUNTIF(C:C,"notconnec")')
        summary_sheet.write(2, 11, '=COUNTIF(C:C,"connected")')
        summary_sheet.write(3, 11, '=COUNTIF(C:C,"disabled")')
        summary_sheet.write(1, 10, "notconnec")
        summary_sheet.write(2, 10, "connected")
        summary_sheet.write(3, 10, "disabled")
        chart= workbook.add_chart({"type":"pie"})
        chart.add_series({"values":"=Summary!L2:L4","categories":"=Summary!K2:K4"})
        summary_sheet.insert_chart("I1",chart)

            
workbook=xlsxwriter.Workbook("interface_status.xlsx")
file=open("switch_list.txt","r")

IP_maker=file.readlines()
IP_address_list=[]
maker=[]
global row_global
row_global=0
summary_sheet = workbook.add_worksheet("Summary")
for makers in IP_maker:
        makers=makers.split("\t")
        print makers
        IP_address_list.append(makers[0])
        print makers
        makers[1]=makers[1].replace("\n","")
        maker.append(makers[1])
for IP_address in IP_address_list:
        global summary_sheet
        data=connection(IP_address,maker[IP_address_list.index(IP_address)])
        response=data_pars(data)
        excel(response,IP_address)
        row_global=summary(response,IP_address,row_global,summary_sheet)
chart()
file.close
workbook.close()
