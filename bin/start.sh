#!/bin/bash

# function gen_stream_asx()
# {
# 	echo "">../stream.asx
# 	ip_addr=`dig +short myip.opendns.com @resolver1.opendns.com`
# 	echo "<ASX version ='3.0'><TITLE>Stream Player</TITLE><ENTRY><REF HREF=\"http://$ip_addr:8080\"/></ENTRY></ASX>" >../stream.asx
# }
# gen_stream_asx


source $LIBRARY_MAKER_ROOT/config/SERVER-CONFIG

$SERVER_BIN/stop.sh

dig +short myip.opendns.com @resolver1.opendns.com>$TEMP/ip_addr

## Start server

pushd $LIBRARY_MAKER_ROOT
$SERVER_BIN/cgi_server.py >>$SERVER_LOGS/server_log_`date +%m%d%Y`.log 2>&1 &
#python -m CGIHTTPServer >>$SERVER_LOGS/server_log_`date +%m%d%Y`.log 2>&1 &
pid=$!
echo $pid>$TEMP/server_pid
popd
echo "sleeping 6 secs and checking status of server"
sleep 6
ps -ef | grep $pid 
if [ $? -eq 0 ]
then
	echo "`date` : Server started." >>$SERVER_LOGS/server_log_`date +%m%d%Y`.log 
	$SERVER_BIN/cache-monitor.sh >>$SERVER_LOGS/server_log_`date +%m%d%Y`.log 2>&1 &
	sleep 1
	ps -ef | grep `cat $TEMP/cache_monitor_pid` >/dev/null
	if [ $? -eq 0 ]
	then
		echo "`date` : Started cache monitor.">>$SERVER_LOGS/server_log_`date +%m%d%Y`.log
	else
		echo "`date` : WARNING: Could not start cache monitor." >>$SERVER_LOGS/server_log_`date +%m%d%Y`.log
	fi
	$SERVER_BIN/monitor_favorites_queue.sh >>$SERVER_LOGS/server_log_`date +%m%d%Y`.log 2>&1 &
	sleep 1
	ps -ef | grep `cat $TEMP/monitor_fav_q_pid` >/dev/null
	if [ $? -eq 0 ]
	then
		echo "`date` : Favorites queue monitor started." >>$SERVER_LOGS/server_log_`date +%m%d%Y`.log
	else
		echo "`date` : WARNING: Could not start Favorites queue monitor." >>$SERVER_LOGS/server_log_`date +%m%d%Y`.log
	fi
	$SERVER_BIN/monitor_library.sh >>$SERVER_LOGS/server_log_`date +%m%d%Y`.log 2>&1 &
	sleep 1
	ps -ef | grep `cat $TEMP/monitor_lib_pid` >/dev/null
	if [ $? -eq 0 ]
	then
		echo "`date` : Started Library monitor" >>$SERVER_LOGS/server_log_`date +%m%d%Y`.log
	else
		echo "`date` : WARNING: Could not start library monitor." >>$SERVER_LOGS/server_log_`date +%m%d%Y`.log
	fi
	$SERVER_BIN/monitor_ffmpeg_queue.sh >>$SERVER_LOGS/server_log_`date +%m%d%Y`.log 2>&1 &
	sleep 1
	ps -ef | grep `cat $TEMP/monitor_ffmpeg_q_pid` >/dev/null
	if [ $? -eq 0 ]
	then
		echo "`date` : Started ffmpeg queue monitor" >>$SERVER_LOGS/server_log_`date +%m%d%Y`.log
	else
		echo "`date` : WARNING: Could not start ffmpeg queue monitor" >>$SERVER_LOGS/server_log_`date +%m%d%Y`.log
	fi
	exit 0
else
	echo "failed to start server check the logs"
	rm $TEMP/server_pid
	exit 1
fi
