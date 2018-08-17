import socket

f=open("hostnames.txt","r")
fw=open("resolve_host.txt","w")
host=f.readlines()
command=raw_input("would you like convert ip to hostname?'0' or hostname to ip? '2'")
command=int(command)
for hostname in host:
        hostname=hostname.replace("\n","")
        print hostname
        try:
                ip=socket.gethostbyaddr(hostname)
                ip=str(ip[command])
                ip=ip.replace("'","")
                ip=ip.replace("[","")
                ip=ip.replace("]","")
                print ip
                fw.write(str(ip)+"\n")
        except:
                pass
