#!/usr/bin/python

import sys
import json
import os

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

def loadLib():
	lib_json = server_config['DATA_ROOT'] + "/lib.json"
	f_lib_json = open(lib_json,'r')
	v_lib_json = json.load(f_lib_json)
	return v_lib_json


vid = str(sys.argv[1])
server_config=loadServerConfig()
lib=loadLib()
print lib[vid]["filepath"]