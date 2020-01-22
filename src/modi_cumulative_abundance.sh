#!/bin/bash
# Calculates the cumulative percentage for input column

# This is the modified version by Jia to get the cumulative score instead of cumulative abundance (1/13/2020)

# Usage: bash modi_cumulative_abundance.sh inputfile.txt column_number 

# exit when any command fails
set -e

bold=$(tput bold)
normal=$(tput sgr0)

die() {
	printf 'ERROR: %s\n' "$1"
	printf 'See modi_cumulative_abundance for help. \n' >&2
	exit 1
}


usage() { cat << EOF

${bold}mfpcount: modi_cumulative_abundance${normal}

Calculate the cummulative abundance of each value in a given column in a given
input file

${bold}Usage:${normal} modi_cummulative_abundance <input_file> <input_column>

${bold}Inputs:${normal}
	- input_file: An input file with columns: gene, richness, abundance,
	  s_score
	- input_column: An integer which is bigger than 0 and smaller than or
	  equal to the total number of columns in input file

${bold}Outputs:${normal}
	- Assuming values in the given column are numbers ranked in a
	  descending order, cumulative percentage with each value is calculated

${bold}Example:${normal} modi_cumulative_abundance input.tsv 4 


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


#echo $input_file
#echo $in_col
#echo $new_in_col

#awk '{print $4}' $input_file
#awk -v temp=$in_col '{print $temp}' $input_file

total_abundance="$(awk -v temp1=$in_col '{sum+=$temp1}END{print sum}' $input_file)"
#echo $total_abundance

awk -v var=$total_abundance -v temp2=$in_col 'BEGIN{OFS="\t"}{sum+=$temp2;print $0 OFS substr(sum/var, 1, 5)}' $input_file
