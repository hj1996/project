#! /usr/bin/python
#this script connects to router and switches and changes the enable password for brocade switches 

import paramiko
import socket
import time

def connection(IP_address,enable_pass,new_enable,new_super_user,new_pass):
#This function connects to a Brocade switch and runs commands on it to change the enable password 
        username = ""
        password = ""
        ssh=paramiko.SSHClient() #prepairs the first session
        ssh2=paramiko.SSHClient() #prepairs the second session
        debug=""  #holds the raw output
        IP_address=IP_address.replace("\n","") #remove the newline char
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
                ssh.connect(IP_address, username=username,password=password) #starts the first connection
                ssh2.connect(IP_address, username=username,password=password) #starts the second connection
                shell=ssh.invoke_shell() 
				#creates a shell that allows for mutiple commands to be run in one session
                shell_2=ssh2.invoke_shell()
                shell.send("enable\n") 
				#sends the enable command the \n excuted it 
                time.sleep(1) #wait for the command to be excuted 
                data=shell.recv(9999)
				#recives the data
                print data        
                debug=debug+data #store the output for later
                shell.send(enable_pass+"\n")
                time.sleep(1)  #same as before
                data=shell.recv(9999)
                print data
                debug=debug+data
                if "Error - incorrect password" in data:
                        shell.send("enable\n") 
                        shell.send(new_pass+"\n")
                        time.sleep(1)  #same as before
                        data=shell.recv(9999)
                        print data
                        debug=debug+data
                        if "#" in data:
                                status="password was already changed"
                                csv(status,IP_address,debug)
                                ssh.close()
                                ssh2.close()
                                return status
                        else:
                                status="wrong enable- please check the switch"
                                csv(status,IP_address,debug)
                                ssh.close()
                                ssh2.close()
                                return status
                                
                shell.send("conf t \n")
                time.sleep(1)
                data=shell.recv(9999)
                print data
                debug=debug+data
                shell.send("enable telnet password 8 "+new_enable+"\n")
                time.sleep(1)
                data=shell.recv(9999)
                print data
                debug=debug+data
                shell.send("enable super-user-password 8 "+new_super_user+"\n")
                time.sleep(1)
                data=shell.recv(9999)
                print data
                debug=debug+data
                shell_2.send("enable\n")
                time.sleep(1)
                data_2=shell_2.recv(9999)
                print data_2
                debug=debug+data_2
                shell_2.send(new_pass+"\n") 
				#session session tries to login with the new password
                time.sleep(1)
                data_2=shell_2.recv(9999)
                print data_2
                debug=debug+data_2
                if "Error - incorrect password" in data_2:
				#if the second session fails to login the first session tries to change to password again
                        shell.send("enable telnet password 8 "+new_enable+"\n")
                        time.sleep(1)
                        data=shell.recv(9999)
                        print data
                        debug=debug+data
                        shell.send("enable super-user-password 8 "+new_super_user+"\n")
                        time.sleep(1)
                        data=shell.recv(9999)
                        print data
                        debug=debug+data
                        shell_2.send("enable\n")
                        time.sleep(1)
                        data_2=shell_2.recv(9999)
                        print data_2
                        shell_2.send(new_pass+"\n")
                        time.sleep(1)
                        data_2=shell_2.recv(9999)
                        print data_2
                        debug=debug+data_2
                        if "Error - incorrect password" in data_2:
						#if the second attempt to change the password fails 
                               status="fail to change password please check switch"
                        else:
                                shell.send("exit\n")
                                time.sleep(1)
                                data=shell.recv(9999)
                                print data
                                debug=debug+data
                                shell.send("wr mem\n") #save the changes
                                time.sleep(1)
                                data=shell.recv(9999)
                                print data
                                debug=debug+data
                                shell.send("\n")
                                time.sleep(1)
                                data=shell.recv(9999)
                                print data
                                debug=debug+data
                                status="enable password change was successful"      
                else:
                        shell.send("exit\n")
                        time.sleep(1)
                        data=shell.recv(9999)
                        print data
                        debug=debug+data
                        shell.send("wr mem\n") #save the changes
                        time.sleep(1)
                        data=shell.recv(9999)
                        print data
                        debug=debug+data
                        shell.send("\n")
                        time.sleep(1)
                        data=shell.recv(9999)
                        print data
                        debug=debug+data
                        status="enable password change was successful"
                shell.send("exit\n")
                time.sleep(1)
                data=shell.recv(9999)

        except paramiko.AuthenticationException:  #various error handling 
                status="AuthenticationException"
        except paramiko.ssh_exception.NoValidConnectionsError:
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
#this function handles saving the result to a csv file
        print resp
        debug=debug.replace("\n","")
        debug=filter(None,debug) #cleans the data
        file_db.write(debug+"\n")#writes the raw output to a file
        try:
		#tries to resolve the ip address to a host name 
            host_name=socket.gethostbyaddr(ip_address)
            host_name=host_name[0]
        except:
            host_name="not able to resolve"
        print host_name
        f_out.write(str(resp)+","+str(ip_address)+","+str(host_name)+"\n")            


f_out=open("results_brocade.csv","w")
f=open("switch_list_brocade.txt","r") #opens and creates needed files
file_db=open("debug_report_brocade.txt","w")
f_out.write("result,ip address,host name\n")
IP_address_list=f.readlines()
respones="no"
while "y" not in respones.lower():
#gets the user's output
        enable_pass=raw_input("What is the enable password? ")
        new_enable=raw_input("What do you want to change the telnet password to? ")
        new_super_user=raw_input("What do you want to change the super-user-password to? ")
        new_pass=raw_input("What do you want to change the enable password to? ")
        respones=raw_input("Are you sure you want to change the telnet password to "+new_enable+" and super-user-password to"+new_super_user+"? (y/n)")
        
fraction=len(IP_address_list)
ctr=1
for IP_address in IP_address_list:
        print "checking "+str(ctr)+"/"+str(fraction)+"\n"
        ctr+=1
        try:
                data=connection(IP_address,enable_pass,new_enable,new_super_user,new_pass)
        except:
                f_out.write("unknown error"+","+str(IP_address)+","+"\n")
f.close
f_out.close
