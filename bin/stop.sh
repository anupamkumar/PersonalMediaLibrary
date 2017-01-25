#!/bin/bash
source $LIBRARY_MAKER_ROOT/config/SERVER-CONFIG

## Stop cache monitor
kill -9 `cat $TEMP/cache_monitor_pid` 2>/dev/null

##Stop favorites queue monitor
kill -9 `cat $TEMP/monitor_fav_q_pid` 2>/dev/null
kill -9 `cat $TEMP/ffmpeg_pid_fav_q` 2>/dev/null
if [ $? -eq 0 ]
then
	rm -r $VIDEO_CACHE/d_stream_`cat $TEMP/ffmpeg_stream_d_fav_q` 2>/dev/null
fi

##Stop ffmpeg queue monitor
kill -9 `cat $TEMP/monitor_ffmpeg_q_pid` 2>/dev/null

## Stop server
kill -9 `cat $TEMP/server_pid` 2>/dev/null

## stop any orphan listeners 
lsof -i -P | grep -i "8000" | grep "bash" | awk -F' ' '{print $2}' | xargs kill -9 2>/dev/null


## kill any running ffmpeg processes and delete the incomplete stream trancoding
for ffmpeg_proc in `cat $TEMP/ffmpeg_vid_map | cut -d';' -f1`
do
	kill -9 $ffmpeg_proc 2>/dev/null
	if [ $? -eq 0 ]
	then
		rm -r $VIDEO_CACHE/d_stream_`cat $TEMP/ffmpeg_vid_map | grep "$ffmpeg_proc" | cut -d';' -f2` 2>/dev/null
	fi
done

## clean up flies

rm $SERVER_PLAYER_PATH/stream-player*.html 2>/dev/null
rm $TEMP/* 2>/dev/null

##Stop library monitor
ps -ef | grep "monitor_library.sh" | grep -v "grep"
if [ $? -eq 0 ]
then
touch $TEMP/kill_monitor_lib_flag
fi