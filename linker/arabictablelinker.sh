#!/bin/sh

# Adds anchors to HTML file of Arabic notes table
# Invoke using one argument: string input_file
# Example: ./arabictablelinker.sh Diary_47_Arabic.html

if [ "1" -eq $# ]
then
    # ADD_PPP_LL:XXX
    sed -i.bak 's/\(A[0-9]\{2\}_[0-9]\{3\}_[0-9]\{2\}\)\:([0-9]\{3\}\)/<a name=\"\2\">\1:\2<\/a>/g' $1
else
    echo 'Usage: arabiclinkgen_table.sh <input_file>'
fi