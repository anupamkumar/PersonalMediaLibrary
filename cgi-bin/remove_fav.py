#!/usr/bin/python

import cgi
import os
import json
import sys

def loadServerConfig():
	server_config_location=os.environ["LIBRARY_MAKER_ROOT"]+"/config/SERVER-CONFIG"
	f_server_config=open(server_config_location,"r")
	lines = f_server_config.readlines()
	f_server_config.close()
	server_config = {}
	for line in lines:
		key_values=line.split("=")
		if len(key_values) != 2:
			continue
		server_config[key_values[0]]=key_values[1].replace("\n","")
	for item in server_config.keys():
		while "$" in server_config[item]:
			t=server_config[item].split("/")
			for i in range(len(t)):
				if "$" in t[i]:
					t[i] = t[i].replace("$","")
					t[i] = server_config[t[i]]
			server_config[item] = "/".join(t)
	return server_config

def load_list(filename):
	try:
		f = open(filename,'r')
		fl = f.readlines()
		nfl = []
		for i in fl:
			nfl.append(i.replace("\n",""))
		f.close()
		return nfl
	except:
		return None

def save_list(list_name,filename):
	try:
		f = open(filename,'w')
		for item in list_name:
			f.write(item+"\n")
		f.close()
		return 0
	except:
		return -1

def update_lib():
	try:
		f_lib = open(server_config['DATA_ROOT']+"/lib.json","r")
		lib_json = json.load(f_lib)
		f_lib.close()
		item_obj = lib_json[video_id_to_remove]
		item_obj["favorite"] = "no"
		lib_json[video_id_to_remove] = item_obj
		j_lib_json = json.dumps(lib_json)
		try:
			f_lib = open(server_config['DATA_ROOT']+"/lib.json","w")
			f_lib.write(j_lib_json)
			f_lib.close()
			return "ok"
		except:
			return None
	except:
		return None

server_config=loadServerConfig()
fav_list=load_list(server_config['DATA_ROOT']+"/favs.json")
if fav_list != None:
	video_id_to_remove = cgi.FieldStorage()["vid"].value
	fav_list.remove(video_id_to_remove)
	status=save_list(fav_list,server_config['DATA_ROOT']+"/favs.json")
	if status != None:
		update_stat=update_lib()
		if update_stat != None:
			print "Content-Type: text/plain"
			print ""
			print "ok"
		else:
			print "Content-Type: text/plain"
			print ""
			print "Fail"
	else:
		print "Content-Type: text/plain"
		print ""
		print "Fail"
else:
	print "Content-Type: text/plain"
	print ""
	print "Fail"