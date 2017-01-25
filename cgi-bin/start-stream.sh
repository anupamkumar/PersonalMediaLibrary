#!/bin/bash

# uri=$(echo "$QUERY_STRING" | sed -n 's/^.*vn=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
# title=$(echo "$QUERY_STRING" | sed -n 's/^.*t=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
vid=$(echo "$QUERY_STRING" | sed -n 's/^.*id=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
sid=$$

source $LIBRARY_MAKER_ROOT/config/SERVER-CONFIG

uri=`cat $DATA_ROOT/vid_path_map | grep "$vid" | cut -d';' -f1`
title=`echo $uri | rev | cut -d'/' -f1 | rev | cut -d'.' -f1`

ls $VIDEO_CACHE/d_stream_$vid 
if [ $? -ne 0 ]
then
	echo "dir not found in video cache... creating"
	mkdir -p $VIDEO_CACHE/d_stream_$vid
	echo "">$SERVER_LOGS/ffmpeg_$vid.log
	$FFMPEG_LOCATION/ffmpeg -i "$uri" -c:v libx264 -c:a aac -ac $AUDIO_CHANNELS -strict -2 -crf $CRF -profile:v baseline -maxrate $MAX_BIT_RATE -bufsize $BUFFER_SIZE -pix_fmt $PIXEL_FORMAT -s $VIDEO_SIZE -r $VIDEO_FRAME_RATE -aspect $VIDEO_ASPECT_RATIO -flags -global_header -hls_time $HLS_PACKET_TIME -hls_list_size $HLS_LIST_SIZE -hls_wrap $HLS_WRAP_LIMIT -start_number $HLS_START_FRAME $VIDEO_CACHE/d_stream_$vid/stream_$vid.m3u8 >>$SERVER_LOGS/ffmpeg_$vid.log 2>&1 &
	proc_id=$!
	sleep 2
	ps -ef | grep $proc_id | grep -v "grep" >/dev/null
	if [ $? -eq 0 ]
	then
		echo "$proc_id;$vid" >>$TEMP/ffmpeg_vid_map
		echo Content-type: text/html
		echo
		echo "<HTML><meta http-equiv=\"Refresh\" content=\"1; url=/cgi-bin/stats-collector.py?vid=$vid&sid=$sid\"></HTML>"
	else
		rm -r $VIDEO_CACHE/d_stream_$vid
		echo Content-type: text/html
		echo 
		echo "<HTML><body><h1>ERROR!! Failed to start stream!! Please close this page and try again or try another clip.</h1>"
		echo "<p>debug `date` : Source File: $uri"
		echo "<p>debug `date` : FFMPEG command line:"
		echo "<p>$FFMPEG_LOCATION/ffmpeg -i<br/> \"$uri\"<br/> -c:v libx264<br/> -c:a aac<br/> -ac $AUDIO_CHANNELS <br/>-strict -2 <br/>-crf $CRF <br/>-profile:v baseline -maxrate $MAX_BIT_RATE -bufsize $BUFFER_SIZE -pix_fmt $PIXEL_FORMAT -s $VIDEO_SIZE -r $VIDEO_FRAME_RATE -aspect $VIDEO_ASPECT_RATIO<br/> -flags <br/>-global_header -hls_time $HLS_PACKET_TIME -hls_list_size $HLS_LIST_SIZE -hls_wrap $HLS_WRAP_LIMIT<br/> -start_number $HLS_START_FRAME <br/>$VIDEO_CACHE/d_stream_$vid/stream_$vid.m3u8"
		echo "<p>ERROR: `date` :"
		echo "<p>`cat $SERVER_LOGS/ffmpeg_$vid.log`"
		echo "</body></html>"
	fi
else
	touch $VIDEO_CACHE/d_stream_$vid
	echo Content-type: text/html
	echo
	echo "<HTML><meta http-equiv=\"Refresh\" content=\"1; url=/cgi-bin/stats-collector.py?vid=$vid&sid=$sid\"></HTML>"
fi