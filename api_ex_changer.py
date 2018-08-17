import infoblox
import ipaddress

f=open("extrentiable_attibutes.csv","r")
data=f.readlines()
ex={}
for info in data:
	info=info.split(",")
	ex[info[0]]=info[1]

iba_api = infoblox.Infoblox("", '','', '1.6', 'internal', 'default')
keys=ex.keys()
for key in keys:
	if "network" not in key: 
		update_network_extattrs(,)
	else:
		pass
fw.close()
f.close()


