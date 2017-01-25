#!/usr/bin/python

import json
import io
import os
import sys

server_config={}

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

def load_myjson_v1():
	myjson = {}
	f = open(server_config['DATA_ROOT']+'/myjson.txt')
	txt = f.readlines()
	for line in txt:
		line_map = eval(line)
		line_dict = dict(line_map)
		myjson[line_dict["id"]] = line_dict
	return myjson

def load_prev_myjson():
	return {}

def is_object_indexed(file_obj):
	prev_json = load_prev_myjson()
	for prev_jsons_file_obj in prev_json:
		##convert to sha1 or md5 hash instead of integer number next time
		if(prev_jsons_file_obj == file_obj):
			if prev_jsons_file_obj["indexed"] == True:
				return True
			else:
				if file_obj["indexed"] == True:
					return True
				else:
					return False
	return False

## create file obj corpus and index it
def create_file_obj_corpus(myjson):
	corpus_index = {}
	for i in myjson.keys():
		if is_object_indexed(myjson[i]) == False:
			file_obj = myjson[i]
			corpus = []
			## title into corpus
			try:
				title = file_obj["title"]
				title_terms = title.split(" ")
				for terms in title_terms:
					corpus.append(terms)
				corpus.append(title)
			except:
				pass
			## artists into corpus
			try:
				artists = file_obj["artist"]
				for artist in artists:
					artist_term = artist.split(" ")
					for term in artist_term:
						corpus.append(term)
					corpus.append(artist)
			except:
				pass
			## tags to corpus
			try:
				tags = file_obj["tags"]
				for tag in tags:
					corpus.append(tag)
			except:
				pass
			## file path to corpus
			try:
				filepath = file_obj["filepath"]
				corpus.append(filepath)
				filepath_terms = filepath.split("/")
				for filepath_term in filepath_terms:
					corpus.append(filepath_term)
					filepath_tokens = filepath_term.split(" ")
					for filepath_token in filepath_tokens:
						corpus.append(filepath_token)
			except:
				pass
			## corpus for this file object is ready. create index for this
			corpus = set(corpus)
			##index the corpus into corpus index object
			for corpus_term in corpus:
				corpus_term = corpus_term.lower()
				if corpus_term in corpus_index:
					corpus_term_doc_list = corpus_index[corpus_term]
					if i in corpus_term_doc_list:
						pass
					else:
						corpus_term_doc_list.append(i)
				else:
					corpus_term_doc_list = []
					corpus_term_doc_list.append(i)
					corpus_index[corpus_term] = corpus_term_doc_list
			##mark file object as indexed
			myjson[i]["indexed"] = True
		else:
			myjson[i]["indexed"] = True
	return corpus_index

def update_lib_with_favs(lib):
	f_favs=open(server_config['DATA_ROOT']+"/favs.json")
	l_favs = f_favs.readlines()
	f_favs.close()
	for fav_vid in l_favs:
		try:
			fav_vid = fav_vid.replace("\n","")
			lib[fav_vid]["favorite"] = "yes"
		except:
			sys.stderr.write("could not find fav_vid="+str(fav_vid)+"\n")
	return lib

server_config=loadServerConfig()
myjson = load_myjson_v1()
myjson = update_lib_with_favs(myjson)
print "updating lib JSON completed"
corpus_index = create_file_obj_corpus(myjson)
j_myjson = json.dumps(myjson)
j_ci = json.dumps(corpus_index)
f_lib = open(server_config['DATA_ROOT']+"/lib.json","w")
f_lib.write(j_myjson)
f_lib.close()
f_ci = open(server_config['DATA_ROOT']+"/cindex.json","w")
f_ci.write(j_ci)
f_ci.close()
print "index built"