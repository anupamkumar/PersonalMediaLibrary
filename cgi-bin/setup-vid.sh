#!/bin/bash

source $LIBRARY_MAKER_ROOT/config/SERVER-CONFIG
ipaddr=`cat $TEMP/ip_addr`

vid=$(echo "$QUERY_STRING" | sed -n 's/^.*vid=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
sid=$(echo "$QUERY_STRING" | sed -n 's/^.*sid=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
vid_name=`cat $DATA_ROOT/vid_path_map | grep "$vid" | cut -d';' -f1`
title=`echo "$vid_name" | rev| cut -d'/' -f1 | cut -d'.' -f2- | rev`
echo "<!DOCTYPE html><html><head><link rel=\"stylesheet\" href=\"/client/static/flowplayer-6.0.5/skin/functional.css\"><script src=\"/client/static/flowplayer-6.0.5/jquery-1.12.4.min.js\"></script><script src=\"/client/static/flowplayer-6.0.5/flowplayer.min.js\"></script><script src=\"/client/static/flowplayer-6.0.5/flowplayer.hlsjs.min.js\"></script><title>Player : $title</title></head><body><div><h3>$title</h3></div><div id=\"player\"><div data-live=\"false\" data-ratio=\"0.5625\" class=\"flowplayer fixed-controls\" data-volume=\"0\" style=\"max-width: 800px; max-height: 450px;\"><video data-title=\"$title\"><source type=\"application/x-mpegurl\" src=\"http://$ipaddr:8000/$CLIENT_PATH_TO_VIDEO_CACHE/d_stream_$vid/stream_$vid.m3u8\"></video></div><p hidden id=\"vid\">$vid</p></div><p>&nbsp;</p><p><div><form method=\"GET\" action=\"/cgi-bin/stop.sh?vid=$vid\"><input type='submit' value='stop'></input></form></p></body></html>" >$SERVER_PLAYER_PATH/stream-player_$sid.html

echo Content-type: text/html
echo
echo "<html><body><p hidden id=\"vid\">$vid</p><p hidden id=\"sid\">$sid</p><script src=$CLIENT_JS_LOCATION/check-stream-init.js></script><div id='content'></div><div id='progress'></div><script type='text/javascript'>start();</script></body></html>"