#!/usr/bin/python

import os
import json
import cgi

## global variables
vidId_playCount_map= {}
server_config={}
vid = cgi.FieldStorage()["vid"].value
sid= cgi.FieldStorage()["sid"].value


## common functions
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

## load exiting playCount first
def load_vidId_playCount_map():
	global server_config
	try:
		f_vidId_playCount_map=open(server_config['DATA_ROOT']+'/vidId_playCount_map.json','r')
		vidId_playCount_map = json.load(f_vidId_playCount_map)
		f_vidId_playCount_map.close()
		return dict(vidId_playCount_map)
	except:
		print "WARNING: cound not load vidId_playCount_map.json."
		return dict({})

## increment playcount of vidId by 1
def increment_playcount(vid):
	global vidId_playCount_map
	vid = str(vid)
	if vid in vidId_playCount_map.keys():
		cur_cnt = vidId_playCount_map[vid]
		cur_cnt = cur_cnt + 1
		vidId_playCount_map[vid] = cur_cnt
	else:
		vidId_playCount_map[vid] = 1

## save the updated vidId PlayCount map to file
def save_vidId_playCount_map():
	global vidId_playCount_map
	global server_config
	try:
		f_vidId_playCount_map=open(server_config['DATA_ROOT']+'/vidId_playCount_map.json','w')
		json.dump(vidId_playCount_map,f_vidId_playCount_map)
		f_vidId_playCount_map.close()
	except:
			print "WARNING: could not save vidId_playCount_map.json"

### script start ### 
server_config=loadServerConfig()
vidId_playCount_map=load_vidId_playCount_map()
increment_playcount(vid)
save_vidId_playCount_map()
print "Content-Type: text/html"
print ""
print "<HTML><meta http-equiv=\"Refresh\" content=\"1; url=/cgi-bin/setup-vid.sh?vid="+vid+"&sid="+sid+"\"></HTML>"
