#!/bin/sh

# Adds links from diary's arabic notes to appropriate place in arabic notes table
# Invoke using two arguments: string input_file, string table_url
# Example: ./arabicdiarylinker.sh Diary_47_20150428.html http://depts.washington.edu/newbook/Diary_47_Arabic.html

if [ "2" -eq $# ]
then
    # ADD_PPP_LL:XXX
    sed -i.bak "s@\(A[0-9]\{2\}_[0-9]\{3\}_[0-9]\{2\}\):\([0-9]\{3\}\)@<a href=\"$2#\2\">\1:\2<\/a>@g" $1
else
    echo 'Usage: arabicdiarylinker.sh <input_file> <table_url>'
fi