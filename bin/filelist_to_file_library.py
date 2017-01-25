#!/usr/bin/python
##### 
### to get filelist --> find . -type f | grep -vi "jpg$" | grep -vi "png$" | grep -vi "gif$" | grep -vi "bmp$" | grep -vi "jpeg$" | grep -vi "m4a$" | grep -vi "db$" >~/Desktop/library_maker/server/filelist.list
#####
#### Script to break down file name into a more human readable , browsable list . 
## List will be formatted in JSON so that Client Side JS can work on it directly.
## fields / keys in JSON for each file :
# {
#	id:
#	filepath: 
#	title:
#	artist: []
#	tags: []
#	store-sites: []
#	publish-date:
#	index-datetime:
#   favorite: <yes/no>
# }
## NOTE: this script will not target to fill all the fields mentioned above, specially the arrays. Eg: Tags , store-sites, publish date will not be filled. 
## eg: ./Z Clips/ObeyAriella - Simona Obeys Ariella.avi
# {
#	id: 
#	filepath: "./Z Clips/ObeyAriella - Simona Obeys Ariella.avi"
#	title: "Simona Obeys Ariella"
#	artist: ["Z Clips", "ObeyAriella"]
# }

##Load file names with english characters
# skip and log the files that don't have other characters 

import operator
import re
import os
import hashlib
from multiprocessing import Process

g_artist_list = []
g_title_list = []
g_id = 0
server_config= {}
g_f_sig_map = {}

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

def load_known_artists():
	global g_artist_list
	f=open('known-artists-list','r')
	artists=f.readlines()
	for artist in artists:
		g_artist_list.append(artist)



def load_file_list():
	f=open(server_config['DATA_ROOT']+"/filelist.delta.list",'r')
	files = f.readlines()
	f.close()
	en_files = []
	other_files = []
	for file in files:
		if isEnglish(file):
			en_files.append(file[:-1])
		else:
			other_files.append(file)
	f=open(server_config['DATA_ROOT']+'/other_files.list','a')
	for file in other_files:
		f.write(file)
	f.close()
	return en_files

def isEnglish(s):
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def removeStopWords(word_list):
	f = open(server_config['DATA_ROOT']+'/stop-words.txt','r')
	swl = f.read().split('\n')
	f.close()
	if type(word_list) is dict:
		new_word_list = {}
		for word in word_list.keys():
			if word in swl:
				# print "'" + word + "' found in swl.skipping"
				pass
			else:
				# print "'" + word + "' not found in swl. safe to add"
				new_word_list[word] = word_list[word]
		sorted_wl = sorted(new_word_list.items(), key=operator.itemgetter(1))
		return sorted_wl
	elif type(word_list) is list:
		new_word_list = []
		for word in word_list:
			if word in swl:
				pass
			else:
				new_word_list.append(word)
		return word_list

def prepare_file_obj(en_file):
	global g_artist_list;
	global g_title_list;
	file_obj = {}
	file_obj["filepath"] = en_file
	file_obj["artist"] = []
	file_obj["id"] = get_sha1_sig(en_file)
	if len(en_file.split("/")) > 1:
		tokens = en_file.split("/")
		for i in range(0,len(tokens)):
			if i < len(tokens)-1:
				# subtokens = tokens[i].split("-")
				# for st in subtokens:
				if tokens[i] in dict_list:
					pass
				else:
					file_obj["artist"].append(lines2spaces(tokens[i]).lower())
				# g_artist_list.append(lines2spaces(tokens[i].lower()))
			else:
				# subtokens = tokens[i].split("-")
				# for j in range(0,len(subtokens)):
					# if j < len(subtokens)-1:
				# file_obj["artist"].append(subtokens[j])
					# else:
				temp = tokens[i].split(".")
				word = ""
				for i in range(0,len(temp)-1):
					word = word + " " + temp[i]
				file_obj["title"] = lines2spaces(camelCase2spaces(word))
				# g_title_list.append(lines2spaces(camelCase2spaces(word).lower()))
				file_obj["tags"] = list(set(generate_tags(lines2spaces(camelCase2spaces(word).lower())).keys()))
				predicted_artists_list = list(set(predict_artists(lines2spaces(camelCase2spaces(word).lower()))))
				for a in predicted_artists_list:
					if len(a) > 0:
						file_obj["artist"].append(a)
	try:
		file_obj["artist"].remove("")
	except:
		pass
	return file_obj;

def predict_artists(terms):
	global g_artist_list
	lterms=[]
	lterms.append(terms)
	# print "lterms = "
	# print lterms
	pa = removeStopWords(lterms)
	# print "removeStopWords ="
	# print pa
	pa = remove_numbers_from_list(pa)
	pa = remove_words_less_than_3_letters(pa)
	pa = get_nouns(pa)
	for a in pa:
		g_artist_list.append(a)
	# print "pa = "
	# print pa
	return pa 

def camelCase2spaces(str):
	new_word = ""
	for j in range(0,len(str)):
		try:
			if str[j].isupper() == True and str[j+1].islower() == True:
				new_word = new_word + " " + str[j]
			else:
				new_word = new_word + str[j]
		except:
			new_word = new_word + str[j]
	return new_word

def lines2spaces(str):
	str = str.replace("[","")
	str = str.replace("]"," ")
	str = str.replace("(", "")
	str = str.replace(")"," ")
	str= str.replace("_"," ")
	str = str.replace("-"," ")
	str = removeLeadingNumbers(str)
	# print str
	str = ' '.join(str.split())
	return str

def removeLeadingNumbers(str):
	num_flag=True
	new_str=""
	for s in str:
		if s.isalpha():
			new_str = new_str + s
			num_flag = False
		else:
			if num_flag == False:
				new_str = new_str + s
	if len(new_str) == 0:
		new_str = str
	return new_str


def generate_tags(phrase):
	tf={}
	terms = phrase.split(" ")
	for term in terms:
		if term in tf:
			term_cnt = tf[term]
			term_cnt = term_cnt + 1
			tf[term] = term_cnt
		else:
			tf[term] = 1
	if(len(terms) > 1):
		## tuples
		i=0
		while i < len(terms):
			if i+1 < len(terms):
				term = terms[i] + " " + terms[i+1]
			else:
				term = terms[i]
			if term in tf:
				term_cnt = tf[term]
				term_cnt = term_cnt + 1
				tf[term] = term_cnt
			else:
				tf[term] = 1
			i = i + 2
		## triples
		i=0
		while i < len(terms):
			if i+2 < len(terms):
				term = terms[i] + " " + terms[i+1] + " "+terms[i+2]
			elif i+1 < len(terms):
				term = terms[i] + " " + terms[i+1]
			else:
				term = terms[i]
			if term in tf:
				term_cnt = tf[term]
				term_cnt = term_cnt + 1
				tf[term] = term_cnt
			else:
				tf[term] = 1
			i = i + 3
		## quads
		i=0
		while i < len(terms):
			if i+3 < len(terms):
				term = terms[i] + " " + terms[i+1] + " "+terms[i+2] + " " + terms[i+3]
			elif i+2 < len(terms):
				term = terms[i] + " " + terms[i+1] + " "+terms[i+2]
			elif i+1 < len(terms):
				term = terms[i] + " " + terms[i+1]
			else:
				term = terms[i]
			if term in tf:
				term_cnt = tf[term]
				term_cnt = term_cnt + 1
				tf[term] = term_cnt
			else:
				tf[term] = 1
			i = i + 4
	return tf

def findTF(t_list):
	tf={}
	for phrase in t_list:
		terms = phrase.split(" ")
		for term in terms:
			if term in tf:
				term_cnt = tf[term]
				term_cnt = term_cnt + 1
				tf[term] = term_cnt
			else:
				tf[term] = 1
		if len(terms) > 1:
			## tuples
			i=0
			while i < len(terms):
				if i+1 < len(terms):
					term = terms[i] + " " + terms[i+1]
				else:
					term = terms[i]
				if term in tf:
					term_cnt = tf[term]
					term_cnt = term_cnt + 1
					tf[term] = term_cnt
				else:
					tf[term] = 1
				i = i + 2
			## triples
			i=0
			while i < len(terms):
				if i+2 < len(terms):
					term = terms[i] + " " + terms[i+1] + " "+terms[i+2]
				elif i+1 < len(terms):
					term = terms[i] + " " + terms[i+1]
				else:
					term = terms[i]
				if term in tf:
					term_cnt = tf[term]
					term_cnt = term_cnt + 1
					tf[term] = term_cnt
				else:
					tf[term] = 1
				i = i + 3
			## quads
			i=0
			while i < len(terms):
				if i+3 < len(terms):
					term = terms[i] + " " + terms[i+1] + " "+terms[i+2] + " " + terms[i+3]
				elif i+2 < len(terms):
					term = terms[i] + " " + terms[i+1] + " "+terms[i+2]
				elif i+1 < len(terms):
					term = terms[i] + " " + terms[i+1]
				else:
					term = terms[i]
				if term in tf:
					term_cnt = tf[term]
					term_cnt = term_cnt + 1
					tf[term] = term_cnt
				else:
					tf[term] = 1
				i = i + 4
	sorted_tf = sorted(tf.items(), key=operator.itemgetter(1))
	return sorted_tf

def tf_stats(tf):
	ctr = 0
	sum = 0
	for key,val in tf:
		sum = sum + val
		ctr = ctr + 1
	print "total number of terms"
	print sum
	print "total number of terms"
	print ctr
	print "dict length"
	print len(tf)
	print "avg occurance of a term"
	print sum/ctr

def extract_title_artist_studio(en_file_list):
	file_ob_list = []
	for en_file in en_file_list:
		print "processing en_filename: "+en_file
		file_obj = prepare_file_obj(en_file)
		file_ob_list.append(file_obj)
		print "done"
	return file_ob_list

### words found in dictionary are not nouns
def get_nouns(term_list):
	noun_terms_list = []
	try:
		f = open(server_config['DATA_ROOT']+"/nouns.txt","r")
		noun_terms_list = f.read().split('\n')
		f.close()
		return noun_terms_list
	except:
		# load english words file
		dict_file = open(server_config['DATA_ROOT']+"/en_dict.txt","r")
		dict_list = dict_file.read().split('\n')
		# print "loaded dict_list: dictsize = "
		# print len(dict_list)
		dict_file.close()
		i = 0
		tot = len(term_list)
		# print "term list = "
		# print term_list
		for term in term_list:
			# print "term ="
			# print term
			# if(i % 1000 == 0):
				# print "term " + str(i) + "/" + str(tot) + " processed"
			tokens = term.split(' ')
			noun_term = []
			temp = []
			noun_term_enc = False
			noun_aldy_written = False
			for token in tokens:
				if token.isalpha() == False:
					pass
				temp.append(token)
				if token in dict_list:
					if noun_term_enc == True:
						noun_aldy_written = True
						for t in temp:
							if t == temp[len(temp)-1]:
								pass
							else:
								noun_term.append(t)
						temp = []
						if len(noun_term) > 0:
							noun_terms_list.append(" ".join(noun_term))
							noun_term = []
				else:
					noun_term_enc = True
			# print "noun_term_enc = "+ str(noun_term_enc)
			# print "noun_aldy_written = " + str(noun_aldy_written)
			if noun_term_enc == True and noun_aldy_written == False:
				for t in temp:
					noun_term.append(t)
			if len(noun_term) > 0:
				noun_terms_list.append(" ".join(noun_term))
			i = i + 1
		return noun_terms_list

def persist_list_to_file(list,filename):
	f = open(filename,'w')
	for item in list:
		f.write(str(item))
		f.write("\n")
	f.close()

def remove_numbers_from_list(l):
	nl = []
	for st in l:
		nst = remove_numbers_from_string(st)
		if len(nst) > 0:
			nl.append(nst)
	return nl

def remove_numbers_from_string(st):
	new_st = ""
	for cha in st:
		if cha.isdigit():
			pass
		else:
			new_st = new_st + cha
	return new_st

def count_noun_freqs(nouns):
	noun_freq = {}
	for noun in nouns:
		if noun in noun_freq:
			cnt = noun_freq[noun]
			cnt = cnt + 1
			noun_freq[noun] = cnt
		else:
			noun_freq[noun] = 1
	noun_freq = sorted(noun_freq.items(), key=operator.itemgetter(1))
	return noun_freq

def remove_words_less_than_3_letters(ol):
	nl = []
	for w in ol:
		# print "remove_words_less_than_3_letters() w = "+w
		# print "remove_words_less_than_3_letters() len ="+str(len(w))
		if len(w) <= 3:
			# print "remove_words_less_than_3_letters() len ="+str(len(w))+ " is <=3 skipping."
			pass
		else:
			nl.append(w)
	return nl


def get_sha1_sig(file):
	hasher = hashlib.md5()
	hasher.update(file)
	return hasher.hexdigest()

# print get_sha1_sig("/Users/anupamkumar/Library/ff/2016-11-16-sl/_1-sl-o-AngryCruelAndBrutal.mkv")

server_config=loadServerConfig()
dict_file = open(server_config['CONFIG_ROOT']+"/Library_TLD","r")
dict_file_lines = dict_file.readlines()
dict_list = []
for line in dict_file_lines:
	t = line.split("/")
	for tt in t:
		dict_list.append(tt)
dict_file.close()
flist= load_file_list()
json = extract_title_artist_studio(flist)
persist_list_to_file(json,server_config['DATA_ROOT']+"/lib.delta.json")
# persist_list_to_file(g_artist_list,"predicted_artist_list.txt")


# def check_if_part_removed_from_nouns(nouns):
# 	for noun in nouns:
# 		if "part" in noun:
# 			return False
# 	return True

# # g_tf = findTF(g_title_list)
# # print g_tf
# g_tf_stoplist = removeStopWords(g_title_list)
# g_tf_stoplist_no_num = remove_numbers_from_list(g_tf_stoplist)
# # print "\n\n\n"
# # print g_tf_stoplist

# persist_list_to_file(g_tf_stoplist_no_num,"tf_without_stopwords.txt")
# pnc = len(g_tf_stoplist_no_num)
# nouns = remove_numbers_from_list(g_tf_stoplist_no_num)
# nouns = remove_words_less_than_3_letters(nouns)
# nouns = get_nouns(g_tf_stoplist)
# nouns = remove_words_less_than_3_letters(nouns)
# round = 2
# while check_if_part_removed_from_nouns(nouns) == False:
# 	print "round "+ str(round)
# 	nouns = get_nouns(nouns)
# 	cnc = len(nouns)
# 	print cnc
# 	if pnc == cnc:
# 		print "exiting since no change in noun cnt"
# 		nouns = remove_numbers_from_list(nouns)
# 		nouns = remove_words_less_than_3_letters(nouns)
# 		break
# 	nouns = remove_numbers_from_list(nouns)
# 	nouns = remove_words_less_than_3_letters(nouns)
# 	round = round + 1
# 	pnc = cnc
# persist_list_to_file(nouns,"nouns.txt")
# # nouns = list(set(nouns))
# noun_freq = count_noun_freqs(nouns)
# print noun_freq
# # persist_list_to_file(nouns,"nouns_without_digits.txt")

# # print n1
# persist_list_to_file(g_title_list,"tl.txt")
# # print nouns



# # noun_freq = count_noun_freqs(nouns)
# # print noun_freq
# # print tf_stats(g_tf)
# # print findTF(g_artist_list)

# # print prepare_file_obj("./weronika/bb-df-sa-lickthatdirtoriwillkickyourballs-A-14m07s-HD1280x720.wmv")