#!/bin/bash

source $LIBRARY_MAKER_ROOT/config/SERVER-CONFIG

$SERVER_BIN/gen_th_vid_path.py
tot_cnt=`cat $DATA_ROOT/vid_path_map | wc -l`
echo "total number of files = $tot_cnt"
for (( cnt=1; cnt<=$tot_cnt; cnt++ ))
do
	echo "entry : $cnt/$tot_cnt"
	entry=`cat $DATA_ROOT/vid_path_map | head -$cnt | tail -1`
	vid=`echo "$entry" | cut -d';' -f2`
	filepath=`echo "$entry" | cut -d';' -f1`
	if [ -d $THUMBNAILS_ROOT/$vid ]
	then
		img_cnt=`ls $THUMBNAILS_ROOT/$vid | wc -l`
		if [ $img_cnt -eq 10 ]
		then
			continue
		else
			rm -r $THUMBNAILS_ROOT/$vid
		fi
	fi
	mkdir -p $THUMBNAILS_ROOT/$vid
	dur=`$FFMPEG_LOCATION/ffmpeg -i "$filepath" 2>&1 | grep "Duration" | cut -d',' -f1 | cut -d":" -f2-`
	echo "Generating thumbnail for $vid ==> $filepath ; dur=$dur"
	$SERVER_BIN/gen_th_ts_snapshots.py "$dur" >$DATA_ROOT/tsl 2>/dev/null
	c=`cat $DATA_ROOT/tsl | wc -l`
	ss=""
	if [ $c -eq 10 ]
	then
		i=0
		while [ $i -lt 10 ]
		do
			timestamp=`head -$((i+1)) $DATA_ROOT/tsl | tail -1`
			ss="$ss -ss $timestamp -vframes 1 -vf scale=320:240 $THUMBNAILS_ROOT/$vid/$i.jpg "
			i=$((i+1))
		done
		$FFMPEG_LOCATION/ffmpeg -i "$filepath" $ss >/dev/null 2>&1
		echo "Done."
	else
		echo "***************************************************************"
		echo "[ERROR] Problem with file $filepath, continuing with next file"
		echo "[DEBUG] entry=$entry"
		echo "[DEBUG] dur=$dur"
		echo "[DEBUG] filepath=$filepath"
		echo "[DEBUG] id=$vid"
	fi
done 