#!/bin/bash

source $LIBRARY_MAKER_ROOT/config/SERVER-CONFIG
rm $DATA_ROOT/filelist.list.temp
# ## get file lists from TLD ##
for tld in `cat ~/Desktop/library_maker/config/Library_TLD`
do
	echo "tld=$tld"
	find "$tld" -type f | grep -vi "jpg$" | grep -vi "png$" | grep -vi "gif$" | grep -vi "bmp$" | grep -vi "jpeg$" | grep -vi "db$" | grep -v ".DS_Store$" | grep -v "zip$" >>$DATA_ROOT/filelist.list.temp
done

## compare with existing filelist ##
$SERVER_BIN/compare2files.py $DATA_ROOT/filelist.list.temp $DATA_ROOT/filelist.list >$DATA_ROOT/filelist.delta.list
cnt=`cat $DATA_ROOT/filelist.delta.list | wc -l`
if [ $cnt -gt 0 ]
then
	## prepare lib delta ##
	$SERVER_BIN/filelist_to_file_library.py 
	## prepare to update lib json file and rebuild index
	cat $DATA_ROOT/lib.delta.json >>$DATA_ROOT/myjson.txt
	$SERVER_BIN/create_index.py
	mv $DATA_ROOT/filelist.list.temp $DATA_ROOT/filelist.list
	rm $DATA_ROOT/filelist.delta.list $DATA_ROOT/lib.delta.json 
fi