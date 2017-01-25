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

def pagify_result():
	output_json= {}
	v_key_list = search_result.keys()
	i_s = int(item_start)
	i_e = i_s + int(page_size)
	for i in range(i_s,i_e):
		try:
			output_json[v_key_list[i]] = search_result[v_key_list[i]]
		except:
			continue
	return json.dumps(output_json)

def loadLib():
	lib_json = server_config['DATA_ROOT'] + "/lib.json"
	f_lib_json = open(lib_json,'r')
	v_lib_json = json.load(f_lib_json)
	return v_lib_json

def doSearch():
	search_index=server_config['DATA_ROOT'] + "/cindex.json"
	f_search_index = open(search_index,'r')
	search_index_json = json.load(f_search_index)
	try:
		id_list = search_index_json[query_str]
	except:
		id_list = []
	begins_with_id_list = []
	for search_term in search_index_json:
		if search_term.startswith(query_str):
			t_id_list = search_index_json[search_term]
			for t_id in t_id_list:
				begins_with_id_list.append(t_id)
	contain_id_list = []
	for search_term in search_index_json:
		if query_str in search_term:
			t_id_list = search_index_json[search_term]
			for t_id in t_id_list:
				contain_id_list.append(t_id)
	combined_id_list = []
	for id_item in id_list:
		combined_id_list.append(id_item)
	for id_item in begins_with_id_list:
		if id_item in combined_id_list:
			continue
		else:
			combined_id_list.append(id_item)
	for id_item in contain_id_list:
		if id_item in combined_id_list:
			continue
		else:
			combined_id_list.append(id_item)
	output = {}
	for id_item in combined_id_list:
		output[id_item] = search_result[id_item]
	return output

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
		return []

def filter_fav():
	fav_ids=load_list(server_config['DATA_ROOT']+"/favs.json")
	output={}
	for fav_id in fav_ids:
		try:
			output[fav_id] = search_result[fav_id]
		except:
			sys.stderr.write(str(fav_id)+" not found in search_result.\n")
			sys.stderr.write(str(fav_id in search_result)+"\n")
			continue
	return output

server_config=loadServerConfig()
## request_type is 
# 1. request entire library
# 2. paged data with data range given
# 3. request fav
# 4. dataset size for fav
try:
	request_type=cgi.FieldStorage()["req"].value
except:
	request_type=1
try:
	item_start=cgi.FieldStorage()["pg_st"].value
except:
	item_start=0
try:
	page_size=cgi.FieldStorage()["pg_size"].value
except:
	page_size=100
try:
	query_str=cgi.FieldStorage()["q"].value
except:
	query_str=""

if query_str != "" and len(query_str) > 1:
	search_result = loadLib()
	search_result = doSearch()
	dataset_size = len(search_result)
else:
	search_result=loadLib()
	dataset_size=len(search_result)

# dataset size
if request_type == "1":
	print "Content-Type: text/plain"
	print ""
	print dataset_size
# paged data
elif request_type == "2":
	print "Content-Type: text/plain"
	print ""
	print pagify_result()
elif request_type == "3":
	search_result = filter_fav()
	dataset_size = len(search_result)
	print "Content-Type: text/plain"
	print ""
	print pagify_result()
elif request_type == "4":
	search_result = filter_fav()
	dataset_size = len(search_result)
	print "Content-Type: text/plain"
	print ""
	print dataset_size
