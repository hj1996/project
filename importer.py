import infoblox
import ipaddress

f=open("extrentiable_attibutes.csv","r")
data=f.readlines()
ex={}
for info in data:
	info=info.split(",")
	ex[info[0]]=info[1]
fw=open("result2.csv","w")
fw.write("sep=;\n")
for line in data:
	if "network" not in line:
		line=line.split(",")
		key=unicode(line[0])
		print key
		ip=ipaddress.IPv4Interface(key)
		ip=ip.with_netmask
		ip=ip.split("/")
		ip=["network"]+ip+[line[1]]+["OVERRIDE"]
		print ip
		for data in ip:
			data=data.replace("\n","")
			fw.write(data)
			fw.write(";")
		fw.write("\n")
	else:
		line=line.split(",")
		header=["header-network","address*","netmask*","EA-"+line[1],"EAInherited-"+line[1]]
		print header
		for data in header:
			data=data.replace("\n","")
			fw.write(data)
			fw.write(";")
		fw.write("\n")

fw.close()
f.close()


