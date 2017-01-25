## monitor ffmpeg process

source $LIBRARY_MAKER_ROOT/config/SERVER-CONFIG

echo $$>$TEMP/monitor_ffmpeg_q_pid

while [ 1 -eq 1 ]
do
	rpc=0
	echo "">$TEMP/ffmpeg_running
	ls $TEMP/ffmpeg_vid_map >/dev/null 2>&1
	if [ $? -eq 0 ]
	then 
		for p in `cat $TEMP/ffmpeg_vid_map`
		do
			ps -ef | grep "`echo $p | cut -d';' -f1`" | grep -v "grep" >/dev/null
			if [ $? -eq 0 ]
			then
				rpc=$((rpc+1))
				echo $p >>$TEMP/ffmpeg_running
			fi
		done
		for rp in `cat $TEMP/ffmpeg_running`
		do
			rpid=`echo $rp | cut -d';' -f1`
			vid=`echo $rp | cut -d';' -f2`
			if [ $rpc -gt $MAX_FFMPEG_PROCS ]
			then
				kill -9 $rpid
				rm -r $VIDEO_CACHE/d_stream_$vid
				rpc=$((rpc-1))
			fi
		done
	fi
done