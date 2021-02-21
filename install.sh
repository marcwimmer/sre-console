#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )


FILE=/usr/local/bin/bot-chat
[[ -f "$FILE" ]] && rm "$FILE"
ln -s "$DIR/chat" "$FILE" 
