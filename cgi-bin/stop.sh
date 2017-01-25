#!/bin/bash

source $LIBRARY_MAKER_ROOT/config/SERVER-CONFIG

vid=$(echo "$QUERY_STRING" | sed -n 's/^.*vid=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")

ff_pid=`cat $DATA_ROOT/ffmpeg_vid_map | grep "$vid" | cut -d';' -f1`

kill -9 $ff_pid

rm -r $VIDEO_CACHE/$vid

echo Content-type: text/html
echo
echo "<script type='text/javascript'>window.close();</script>"