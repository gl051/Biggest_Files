#!/usr/bin/env bash

# -----------------------------------
# Check parameters and set variables
# -----------------------------------
if [ $# -ne 2 ]
then
    echo ''
    echo 'Description: search for the N biggest files starting from the current directory recursively.'
    echo ''
    echo '$ biggest_file dirname n'
    echo
    echo '- dirname is the name of the starting directory'
    echo '- n number of files'
    exit -1
else
    start_dir=$1
    how_many=$2
fi

# Checking directory exists
if [ ! -d "$start_dir" ]
then
    echo "error: first parameter provided is not an existing directory" >&2; exit 1
fi

# Check parameter is a number
if ! [[ $how_many =~ ''^[0-9]+$'' ]]
then
   echo "error: second parameter provided is not a number" >&2; exit 1
fi

# -------------------------------------
# Execution
# -------------------------------------
echo 'Start' $(date +"%r")

current_dir=$(pwd)
cd $start_dir

# list all the  file only and remove extra space, cut the column size and the file name, then sort numerically
# and get the first N
ls -lSR | grep '^-' | tr -s ' ' | cut -d ' ' -f5,9 | sort -n -r  | head -n $how_many

cd $current_dir

echo  'End' $(date +"%r")
