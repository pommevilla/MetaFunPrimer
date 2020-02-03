#!/bin/sh 

shopt -s expand_aliases
test_columns(){
    ACTUAL_COLUMN="$(cat tests/test_data/mfpcount_summary.tsv | cut -f 4)"
    TEST_COLUMN="$(src/calc_sscore tests/test_data/mfpcount_summary.tsv | cut -f 4)"
    ACTUAL_TEST_COLUMNS="$(paste <(echo "$ACTUAL_COLUMN") <(echo "$TEST_COLUMN"))" 
    TEST_STATUS=0

    while read -r actual test
    do
#        if (( $(echo "$actual == $test" | bc -l) )); then
        if (( $(echo "$actual - $test > 0.00001" | bc -l)  )); then
           TEST_STATUS=1
           echo "$actual $test $(echo "$actual - $test" | bc)"
        fi
    done < <(echo "$ACTUAL_TEST_COLUMNS")
    echo "Test status is: $TEST_STATUS"
    assertTrue "Test failed somewhere" "$TEST_STATUS"
} 
  
. shunit2-2.1.7/shunit2
