#! /usr/bin/python
#this script connects to router and switches and changes the enable password 

import paramiko
import socket
import time

def connection(IP_address,enable_pass,new_enable):
        print IP_address
        username = ""
        #username =raw_input("Please enter your username: ")
        #remove the # and add one infront of the username field to allow for manual entry of username
        password = ""
        #password =raw_input("Please enter you password: ")
         #remove the # and add one infront of the password field to allow for manual entry of password
        ssh=paramiko.SSHClient()
        ssh2=paramiko.SSHClient()
        debug=""
        IP_address=IP_address.replace("\n","")
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
                ssh.connect(IP_address, username=username,password=password)#start the first connection
                ssh2.connect(IP_address, username=username,password=password)#start the second connection
                shell=ssh.invoke_shell() 
				#creates the interactive shell that allows for more than one command to be run in one session 
                shell_2=ssh2.invoke_shell()
                shell.send("enable\n") #sends the enable command 
                time.sleep(1) #wait for a second
                data=shell.recv(9999) #recive that data 
                print data
                debug=debug+data
                shell.send(enable_pass+"\n") #input the enable password 
                time.sleep(1)
                data=shell.recv(9999)
                print data
                debug=debug+data
                shell.send("conf t \n") #enter configurate mode
                time.sleep(1)
                data=shell.recv(9999)
                print data
                debug=debug+data
                shell.send("enable secret "+new_enable+"\n") #changes the pass
                time.sleep(1)
                data=shell.recv(9999)
                print data
                debug=debug+data
                shell_2.send("enable\n") #goes into enable more with the second session 
                time.sleep(1)
                data_2=shell_2.recv(9999)
                print data_2
                debug=debug+data_2
                shell_2.send(new_enable+"\n") #tries to login in with the new enable password 
                time.sleep(1)
                data_2=shell_2.recv(9999)
                print data_2
                debug=debug+data_2
                if "% Access denied" in data_2: # if the login change 
                        print "error"
                        shell.send("exit\n")
                        time.sleep(1)
                        data=shell.recv(9999)
                        print data
                        debug=debug+data
                        shell.send("copy startup-config running-config\n") # return to running-config 
                        time.sleep(1)
                        data=shell.recv(9999)
                        print data
                        debug=debug+data
                        shell.send("\n")
                        time.sleep(1)
                        data=shell.recv(9999)
                        print data
                        debug=debug+data
                        status="failed to change the password returning to start up password"
                else: # of the login was successful
                        shell.send("exit\n")
                        time.sleep(1)
                        data=shell.recv(9999)
                        print data
                        debug=debug+data
                        shell.send("copy running-config startup-config\n")
						#save running config
                        time.sleep(1)
                        data=shell.recv(9999)
                        print data
                        debug=debug+data
                        shell.send("\n")
                        time.sleep(1)
                        data=shell.recv(9999)
                        print data
                        debug=debug+data
                        if "Unable to get configuration. Try again later." in data: 
						#specal login error for switches with the bug that prevent the running conf from being saved
                                status="enable password changes was successful but failed to save to start up config"
                        else:
                                status="enable password change was successful"
                shell.send("exit\n")
                time.sleep(1)
                data=shell.recv(9999)

        except paramiko.AuthenticationException:
                status="AuthenticationException"
        except paramiko.ssh_exception.NoValidConnectionsError: # collection of error handling 
                status="NoValidConnectionsError"
        except paramiko.ssh_exception.SSHException:
                status="Incompatible version (1.5 instead of 2.0)"
        except socket.error:
                status="A connection attempt failed because the connected party"
        except:
                status="Unkown error"
        csv(status,IP_address,debug)
        ssh.close()
        ssh2.close()
        return status


def csv(resp,ip_address,debug): 
#this function handles writing the data to a csv file and the debug data in the debug file 
        print resp
        debug=debug.replace("\n","")
        debug=filter(None,debug)
        file_debug.write(debug+"\n")
        try:
            host_name=socket.gethostbyaddr(ip_address)
            host_name=host_name[0]
        except:
            host_name="not able to resolve"
        print host_name
        file_output.write(str(resp)+","+str(ip_address)+","+str(host_name)+"\n")
        
file_output=open("results_cisco.csv","w")
file=open("switch_list_cisco.txt","r")  #opens the needed file 
file_debug=open("debug_report_cisco.txt","w")
file_output.write("result,ip address,host name\n")
IP_address_list=file.readlines()
respones="no"
while "y" not in respones.lower():
        enable_pass=raw_input("What is the enable password? ")
        new_enable=raw_input("What do you want to change the enable password to? ")
        respones=raw_input("Are you sure you want to change the enable password to "+new_enable+"? (y/n)")

for IP_address in IP_address_list:
        try:
                data=connection(IP_address,enable_pass,new_enable)
        except:
             file_output.write("unknown error"+","+str(IP_address)+","+"\n")
file.close
file_output.close
