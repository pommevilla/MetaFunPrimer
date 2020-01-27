#!/bin/bash

#Jia_Liu 1_13_2020

#This tool is to sort rows based on given s-score column, check the value of another given column cumulative s-score, and get all the 
#gene names with cumulatiev s-score not bigger than given threshold
#	1. sort all the lines in an decreasing order based on a given rank column (rank_col; s-score column in this case) with numerical values
#	2. for each line, read and check the numerical value from another given column (cum_s_score_col; cumulative percentage of s-score in this case)
#		1). if the value is smaller than the given threshold: output the value in column1 (gene name)
#		2). output gene name of the first value that is bigger or equal to given threshold; break the loop

#Usage: thresh_tsv input_file rank_col cumulative_s_score_col threshold
#e.g.: thresh_tsv input.tsv 4 5 0.80
#Input:
#	thresh_tsv file
#	rank column
#	column number of cumulative s-score
#	threshold of cumulative s-score (lower limit)
#Output: 
#	recommend_cluster.s_score

# exit when any command fails
set -e

bold=$(tput bold)
normal=$(tput sgr0)

die() {
	printf 'ERROR: %s\n' "$1"
	printf 'See thresh_tsv for help. \n' >&2
	exit 1
}



usage() {
cat << EOF

${bold}mfpcount: thresh_tsv${normal} 

Sort rows based on one given column. Check and compare the value of another
given column with given threshold to get all the gene names with the value
smaller or first equal to the threshold

${bold}Usage:${normal} 
	thresh_tsv <input_file> <ranking_column> <comparing_column> <threshold>

${bold}Inputs:${normal}
	- input_file: An input file with columns: gene, richness, abundance,
	  s_score, cumulative s_score
	- ranking_column: An integer which is bigger than 0 and smaller than or
	  equal to the total number of columns in input file
	- comparing_column: An integer which is bigger than 0 and smaller than
	  or equal to the total number of columns in input file
	- threshold: a number which is bigger than or equal to 0 and smaller
	  than or equal to 1

${bold}Outputs:${normal}
	- for each row, value of column 1 (gene name) will be output if the value of 
		comparing_column was smaller than threshold, or equal to or 
		bigger than the threshold for the first time

${bold}Example:${normal} 
	thresh_tsv input.tsv 4 5 0.80

EOF
}


# Check number of inputs meet the total required arguments number
# (if equal to 4 or not)
if (($#!=4)); then
	usage
	exit 1
fi


#Read input file
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
rank_col=$2

# Test if rank_col is a number and if input_file has at least that many columns
if [[ ! $rank_col =~ ^[1-9]+$ || $rank_col -gt $numCol ]]; then
	die "$0 rank column is out of range"
fi

cum_s_score_col=$3
# Test if comparing_col is a number and if input_file has at least that many columns
if [[ ! $cum_s_score_col =~ ^[1-9]+$ || $cum_s_score_col -gt $numCol ]]; then
	die "$0 comparing column is out of range"
fi

thresh=$4
# Test if thresh is a number and if it's between 0 to 1
if [[ $thresh < 0 || $thresh > 1 ]]; then
	die "$0 threshold should be between 0 and 1"
fi

new_cum_s_score_col="c${cum_s_score_col}"

sort -nrk $rank_col $input_file | while read c1 c2 c3 c4 c5 c6
do 
	echo "${c1}"
	#echo "${c5}"
	# short circuit boolean, can change the order of these conditions
	if [[ ${!new_cum_s_score_col} > $thresh || ${!new_cum_s_score_col} == $thresh ]]; then
	#	echo "$c5"
	#	echo "${!new_cum_s_score_col}"
		break
	fi	
done

