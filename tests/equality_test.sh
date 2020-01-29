#!/bin/sh

testEquality() {
    assertEquals 1 1
}

oneTimeSetUp(){
    echo "Something dumb" > temp_file
}

testFileContents(){
    CONTENTS=$(cat temp_file)
    assertEquals "Contents of temp_file and thing didn't match" "$CONTENTS" "Something dumb"
}

oneTimeTearDown(){
    rm temp_file
}

. ../shunit2-2.1.7/shunit2
