#!/usr/bin/python

import cgi
import os
import json
import sys
g_lines=[]

def loadServerConfig():
	global g_lines
	server_config_location=os.environ["LIBRARY_MAKER_ROOT"]+"/config/SERVER-CONFIG"
	f_server_config=open(server_config_location,"r")
	lines = f_server_config.readlines()
	g_lines = lines
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

def check(line_name):
	for i in range(len(g_lines)):
		if line_name in g_lines[i]:
			return i
	return -1

def replace(name,value,lno):
	global g_lines
	if lno > -1:
		g_lines[lno] = name+"="+value+"\n"

server_config = loadServerConfig()

try:
	tld = cgi.FieldStorage()["tld"].value
	sys.stderr.write("tld="+tld)
	try:
		f_tld = open(server_config['CONFIG_ROOT']+"/Library_TLD","w")
		f_tld.write(tld.replace("!","\n"))
		f_tld.close()
		print "Content-Type: text/plain"
		print ""
		print "1"
	except:
		print "Content-Type: text/plain"
		print ""
		print "-1"
except:
	tld = None
try:
	audio_channels = cgi.FieldStorage()["audio_channels"].value
	server_config['AUDIO_CHANNELS'] = audio_channels
	replace("AUDIO_CHANNELS",audio_channels,check("AUDIO_CHANNELS"))
except:
	audio_channels = None
try:
	crf = cgi.FieldStorage()["crf"].value
	server_config['CRF'] = crf
	replace("CRF",crf,check("CRF"))
except:
	crf = None
try:
	max_bit_rate = cgi.FieldStorage()["max_bit_rate"].value
	server_config['MAX_BIT_RATE'] = max_bit_rate
	replace("MAX_BIT_RATE",max_bit_rate,check("MAX_BIT_RATE"))
except:
	max_bit_rate = None
try:
	buffer_size = cgi.FieldStorage()["buffer_size"].value
	server_config['BUFFER_SIZE']=buffer_size
	replace("BUFFER_SIZE",buffer_size,check("BUFFER_SIZE"))
except:
	buffer_size = None
try:
	pixel_format = cgi.FieldStorage()["pixel_format"].value
	server_config['PIXEL_FORMAT'] = pixel_format
	replace("PIXEL_FORMAT",pixel_format,check("PIXEL_FORMAT"))
except:
	pixel_format = None
try:
	video_size = cgi.FieldStorage()["video_size"].value
	server_config['VIDEO_SIZE']= video_size
	replace("VIDEO_SIZE",video_size,check("VIDEO_SIZE"))
except:
	video_size = None
try:
	video_aspect_ratio = cgi.FieldStorage()["video_aspect_ratio"].value
	server_config['VIDEO_ASPECT_RATIO']=video_aspect_ratio
	replace("VIDEO_ASPECT_RATIO",video_aspect_ratio,check("VIDEO_ASPECT_RATIO"))
except:
	video_aspect_ratio = None
try:
	video_frame_rate = cgi.FieldStorage()["video_frame_rate"].value
	server_config['VIDEO_FRAME_RATE']= video_frame_rate
	replace("VIDEO_FRAME_RATE",video_frame_rate,check("VIDEO_FRAME_RATE"))
except:
	video_frame_rate = None
try:
	hls_packet_time = cgi.FieldStorage()["hls_packet_time"].value
	server_config['HLS_PACKET_TIME']=hls_packet_time
	replace("HLS_PACKET_TIME",hls_packet_time,check("HLS_PACKET_TIME"))
except:
	hls_packet_time = None
try:
	hls_list_size = cgi.FieldStorage()["hls_list_size"].value
	server_config['HLS_LIST_SIZE']=hls_list_size
	replace("HLS_LIST_SIZE",hls_list_size,check("HLS_LIST_SIZE"))
except:
	hls_list_size = None
try:
	hls_wrap_limit = cgi.FieldStorage()["hls_wrap_limit"].value
	server_config['HLS_WRAP_LIMIT']=hls_wrap_limit
	replace("HLS_WRAP_LIMIT",hls_wrap_limit,check("HLS_WRAP_LIMIT"))
except:
	hls_wrap_limit = None
try:
	hls_start_frame = cgi.FieldStorage()["hls_start_frame"].value
	server_config['HLS_START_FRAME']= hls_start_frame
	replace("HLS_START_FRAME",hls_start_frame,check("HLS_START_FRAME"))
except:
	hls_start_frame = None
try:
	max_ffmpeg_procs = cgi.FieldStorage()["max_ffmpeg_procs"].value
	server_config['MAX_FFMPEG_PROCS']=max_ffmpeg_procs
	replace("MAX_FFMPEG_PROCS",max_ffmpeg_procs,check("MAX_FFMPEG_PROCS"))
except:
	max_ffmpeg_procs = None
try:
	cache_max_size = cgi.FieldStorage()["cache_max_size"].value
	server_config['CACHE_MAX_SIZE']=cache_max_size
	replace("CACHE_MAX_SIZE",cache_max_size,check("CACHE_MAX_SIZE"))
except:
	cache_max_size = None

try:
	new_server_config=os.environ["LIBRARY_MAKER_ROOT"]+"/config/SERVER-CONFIG"
	f_new_server_config = open(new_server_config,"w")
	for line in g_lines:
		f_new_server_config.write(line)
	f_new_server_config.close()
	print "Content-Type: text/plain"
	print ""
	print "2"
except:
	print "Content-Type: text/plain"
	print ""
	print "-2"

