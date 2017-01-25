#!/bin/bash

source $LIBRARY_MAKER_ROOT/config/SERVER-CONFIG
echo $$ >$TEMP/monitor_fav_q_pid
while [ 1 -eq 1 ]
do
	echo "`date`: [MONITOR FAVORITES QUEUE] Monitoring favorites queue..."
	for vid in `cat $DATA_ROOT/favs.json`
	do
		myfile=`$SERVER_BIN/vid2vidpath.py $vid`
		
		ls $VIDEO_CACHE/d_stream_$vid >/dev/null 2>&1
		if [ $? -ne 0 ]
		then
			echo "`date` : [MONITOR FAVORITES QUEUE] processing file: $myfile for vid $vid"
			mkdir -p $VIDEO_CACHE/d_stream_$vid
			nice -20 $FFMPEG_LOCATION/ffmpeg -i "$myfile" -c:v libx264 -c:a aac -ac $AUDIO_CHANNELS -strict -2 -crf $CRF -profile:v baseline -maxrate $MAX_BIT_RATE -bufsize $BUFFER_SIZE -pix_fmt $PIXEL_FORMAT -s $VIDEO_SIZE -r $VIDEO_FRAME_RATE -aspect $VIDEO_ASPECT_RATIO -flags -global_header -hls_time $HLS_PACKET_TIME -hls_list_size $HLS_LIST_SIZE -hls_wrap $HLS_WRAP_LIMIT -start_number $HLS_START_FRAME $VIDEO_CACHE/d_stream_$vid/stream_$vid.m3u8 >>$SERVER_LOGS/ffmpeg_$vid.log 2>&1 
			if [ $? -ne 0 ]
			then
				rm -r $VIDEO_CACHE/d_stream_$vid
				echo "`date` : [MONITOR FAVORITES QUEUE] unable to process $myfile for video_id $vid"
			else 
				echo "`date` : [MONITOR FAVORITES QUEUE] done."
			fi
		else
			touch $VIDEO_CACHE/d_stream_$vid
			#echo "`date` : [MONITOR FAVORITES QUEUE] file $myfile already processed."
		fi
	done
	sleep 120
done