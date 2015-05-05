#!/bin/sh

# Adds anchors to HTML file of Arabic notes table
# Invoke using two arguments: string input_file, string output_file
# Example: ./arabiclinkgen_table.sh Diary_47_Arabic.html Diary_47_Arabic_Anchors.html

if [ "2" -eq $# ]
then
    # AN_DD_PPP_LLL:XXX
    sed -i 's/\(AN_[0-9]\{2\}_[0-9]\{3\}_[0-9]\{3\}\)\(:[0-9]\{3\}\)/<a name=\"\2\">\1\2<\/a>/g' $1 > $2
else
    echo 'Usage: arabiclinkgen_table.sh <input_file> <output_file>'
fi