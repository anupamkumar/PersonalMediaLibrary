#!/bin/bash

source $LIBRARY_MAKER_ROOT/config/SERVER-CONFIG
n=`echo "0.2 * $CACHE_MAX_SIZE" | bc | cut -d'.' -f1`

cache_monitor_pid=$$
echo $cache_monitor_pid>$TEMP/cache_monitor_pid

while [ 1 -eq 1 ]
do
	cl=`cat $DATA_ROOT/vidId_playCount_map.json | sed -e 's/[{}]/''/g' | awk -v k="text" '{n=split($0,a,","); for (i=1; i<=n; i++) print a[i]}' | sed -e 's/ //g' | sed -e 's/"//g' | head -$n`
	for i in $cl
	do
		vid=`echo $i | cut -d':' -f1`
		if [ -d $VIDEO_CACHE/d_stream_$vid ]
		then
			touch $VIDEO_CACHE/d_stream_$vid
		fi
	done

	current_cache_size=`ls -1 $VIDEO_CACHE | wc -l`
	favs_size=`cat $DATA_ROOT/favs.json | wc -l`
	cache_max_plus_favs=`expr $CACHE_MAX_SIZE + $favs_size`
	echo "`date` [ CACHE SIZE MONITOR ] Current cache size = $current_cache_size"
	echo "`date` [ CACHE SIZE MONITOR ] Max cache size = $cache_max_plus_favs"
	if [ $current_cache_size -gt $cache_max_plus_favs ]
	then
		over_by=`expr $current_cache_size - $cache_max_plus_favs`
		echo "`date` [ CACHE SIZE MONITOR ] Cache size is over by = $over_by"
		for vdir in `ls -1tr $VIDEO_CACHE`
		do
			if [ $over_by -le 0 ]
			then
				break
			else
				id=`echo $vdir | rev | cut -d'_' -f1 | rev`
				cat $DATA_ROOT/favs.json | grep "$id"
				if [ $? -eq 0 ]
				then
					file=`cat $DATA_ROOT/vid_path_map | grep "$id"`
					echo "`date` [ CACHE SIZE MONITOR ] Deleting $vdir directory. Containing m3u8 for : $file"
					rm -r $VIDEO_CACHE/$vdir
					over_by=`expr $over_by - 1`
				else
					echo "`date` [ CACHE SIZE MONITOR ] $file is a favorite. Cannot delete this."
				fi
			fi
		done
	fi
	sleep 30
done