#!/bin/bash

# Checks to see if the packages required to run MetaFunPrimer packages are
# available for use. Note: This is done through the hash function, so 
# aliases may not evaluate correctly. If you are certain that the programs
# in question are installed and callable, you can ignore the errors and pro-
# ceed with using the pipeline.

join () {
    local IFS="$1"
    shift   
    echo "$*." | sed "s/,/, /g" 
}

echo "MetaFunPrimer"
echo "============="


printf "Checking if required programs are installed and executable.\n\n"

requirements="diamond python blastx cd-hit clustalo-1.2.4-Ubuntu-x86_64 parallel qsub java"

missing_reqs=()
for req in $requirements
do 
    printf "Checking %s: " "$req"
    if hash $req 2>/dev/null
    then
        echo "OK."
    else
        echo "Failed."
        missing_reqs+=("$req")
    fi
done

echo ""

if [ "${#missing_reqs[@]}" -eq 0 ]
then
    echo "All required packages found. MetaFunPrimer is ready for use."
    echo "See https://metafunprimer.readthedocs.io/en/latest/Tutorial.html for an introduction to the pipeline."
else
    printf "Missing requirements: "
    join , ${missing_reqs[@]}
fi

