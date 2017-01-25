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

server_config = loadServerConfig()
request_name = cgi.FieldStorage()["req"].value

if request_name == "TLD":
	f = open(server_config["CONFIG_ROOT"]+"/Library_TLD")
	tld_l = f.readlines()
	print "Content-Type: text/plain"
	print ""
	print "".join(tld_l)
else:
	request_name_u = request_name.upper()
	print "Content-Type: text/plain"
	print ""
	print server_config[request_name_u]