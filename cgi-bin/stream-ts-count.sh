#!/bin/bash
source $LIBRARY_MAKER_ROOT/config/SERVER-CONFIG

vid=$(echo "$QUERY_STRING" | sed -n 's/^.*vid=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
x=`ls $VIDEO_CACHE/d_stream_$vid | wc -l`

echo Content-type: text/html
echo
echo $x