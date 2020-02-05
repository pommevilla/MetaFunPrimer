#!/bin/bash

# In order for this function to calculate the first order difference for s-score instead of abundance, I changed all the original $3 (column for abundance) to $4 (column for s-score)
# Jia 01_14_2020

# I made a second change to this tool so that it can take user input file and user input column number. But I am not quite understand the first order differential yet. So that I do not know how to test this function properly. 
# Jia 01_21_2020

# Usage: modi_fo_diffs <input.txt> <column_number>

# exit when any command fails
set -e

bold=$(tput bold)
normal=$(tput sgr0)

die() {
	printf 'ERROR: %s\n' "$1"
	printf 'See modi_fo_diffs for help. \n' >&2
	exit 1
}

usage() {
cat <<-EOF

${bold}mfpcount: modi_fo_diffs${normal}

Calculate the first order difference to get the 'elbow' for given column in the
given file

${bold}Usage:${normal} modi_fo_diffs <input_file> <input_column>

${bold}Inputs:${normal}
	- input_file: An input file with multiple columns
	- input_column: An integer which is bigger than 0 and smaller than or
	  equal to the total number of columns in input file

${bold}Outputs:${normal}
	- first order difference 

${bold}Example:${normal} 
	modi_fo_diffs input.tsv 4

EOF
}

# Check if number of inputs meet the total required arguments number
# if equals to 2 or not
if (($#!=2)); then
	usage
	exit 1
fi
 
input_file=$1
#TODO: (Do we need this?) Check if input_file exists
if [ ! -f "$input_file" ]; then
	die "$0 file not found."
fi

#Check if file is empty
if [ ! -s "$input_file" ]; then
	die "$0 $input_file is empty."
fi


#Get the number of columns in the input file
numCol=$(head -1 $input_file | awk '{print NF}')
in_col=$2


# Test if rank_col is a number and if input_file has at least that many columns
if [[ ! $in_col =~ ^[1-9]+$ || $in_col -gt $numCol ]]; then
	die "$0 input column is out of range"
fi

info=$(awk -v temp1=$in_col '{
    if(NR==1)
    {
        min = $temp1
        max = $temp1
    }
    if($temp1 < min)
    {
        min = $temp1
    }
     
}
END {
    print min","max
}' $input_file)

awk -v var=$info -v temp2=$in_col '
BEGIN {
    split(var, info, ",")
    min = info[1]
    max = info[2]
    OFS = "\t"
} 
{
    left = (max - $temp2) / NR;
    NR==20 ? right = 0: right = ($temp2 - min) / (20 - NR) 
    print $0 OFS left - right

}' $input_file
