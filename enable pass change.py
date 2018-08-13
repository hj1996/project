#! /usr/bin/python


import paramiko
import xlsxwriter
import socket
import time
def connection(IP_address,enable_pass,new_enable):
        username = ""
        password = ""
        ssh=paramiko.SSHClient()
        ssh2=paramiko.SSHClient()
        IP_address=IP_address.replace("\n","")
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
                ssh.connect(IP_address, username=username,password=password)
                ssh2.connect(IP_address, username=username,password=password)
                shell=ssh.invoke_shell()
                shell_2=ssh2.invoke_shell()
                shell.send("enable\n")
                time.sleep(1)
                data=shell.recv(9999)
                print data        
                shell.send(enable_pass+"\n")
                time.sleep(1)
                data=shell.recv(9999)
                print data
                shell.send("conf t \n")
                time.sleep(1)
                data=shell.recv(9999)
                print data
                shell.send("enable secret "+new_enable+"\n")
                time.sleep(1)
                data=shell.recv(9999)
                print data
                shell_2.send("enable\n")
                time.sleep(1)
                data_2=shell_2.recv(9999)
                print data_2
                shell_2.send(new_enable+"\n")
                time.sleep(1)
                data_2=shell_2.recv(9999)
                print data_2
                if "% Access denied" in data_2:
                        print "error"
                        shell.send("exit\n")
                        time.sleep(1)
                        data=shell.recv(9999)
                        print data
                        shell.send("copy startup-config running-config\n")
                        time.sleep(1)
                        data=shell.recv(9999)
                        print data
                        shell.send("\n")
                        time.sleep(1)
                        data=shell.recv(9999)
                        print data
                        status="failed to change the password returning to start up password"
                else:
                        shell.send("exit\n")
                        time.sleep(1)
                        data=shell.recv(9999)
                        print data
                        shell_2.send("copy running-config startup-config\n")
                        time.sleep(1)
                        data_2=shell.recv(9999)
                        print data_2
                        shell.send("\n")
                        time.sleep(1)
                        data=shell.recv(9999)
                        print data
                        status="enable password change was successful"
                shell.send("exit\n")
                time.sleep(1)
                data=shell.recv(9999)

        except paramiko.AuthenticationException:
                status="AuthenticationException"
        except paramiko.ssh_exception.NoValidConnectionsError:
                status="NoValidConnectionsError"
        except paramiko.ssh_exception.SSHException:
                status="Incompatible version (1.5 instead of 2.0)"
        except socket.error:
                status="A connection attempt failed because the connected party"
        except:
                status="Unkown error"
        csv(status,IP_address)
        ssh.close()
        ssh2.close()
        return status


def csv(resp,ip_address):
        print resp
        f_out.write(str(resp)+","+str(ip_address)+"\n")            


f_out=open("results.csv","w")
f=open("switch_list.txt","r")
f_out.write("result,ip_address\n")
IP_address_list=f.readlines()
respones="no"
while "y" not in respones:
        enable_pass=raw_input("What is the enable password? ")
        new_enable=raw_input("What do you want to change the enable password to? ")
        respones=raw_input("Are you sure you want to change the enable password to "+new_enable+"? (y/n)")

for IP_address in IP_address_list:
        data=connection(IP_address,enable_pass,new_enable)
        
f.close
f_out.close
