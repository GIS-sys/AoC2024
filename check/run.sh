#!/bin/bash

# Function to show usage and error messages
show_error() {
    echo "$1"
    exit 1
}

LONGEST="0m0.000s"

# Function to run command and prettify time and output
pretty_output() {
    . <({ berr=$({ bout=$(bash -c "$1"); } 2>&1; declare -p bout >&2); declare -p berr; } 2>&1)
    echo -e "TIME: $berr"
    echo -e "RESULT: $bout"
    echo ""
    systime=$(echo -e "$berr" | grep "real	")
    systime=${systime#*	}
    if [[ $LONGEST < $systime ]]; then
        LONGEST=$systime
    fi
}

# Function to run a task
run_program() {
    echo "Running ${1}a/main.py with input ${1}"
    pretty_output 'time cat "check/inputs/'${1}'" | python "'${1}'a/main.py"'
    echo "Running ${1}b/main.py with input ${1}"
    pretty_output 'time cat "check/inputs/'${1}'" | python "'${1}'b/main.py"'
}

HELP_MESSAGE="Argument must be a number between 00 and 25 inclusive (always two digits). If 0, will take each input file from check/inputs/ folder and run tasks for them. If not 0, will run specified task only."

# Check number of arguments
if [ "$#" -ne 1 ]; then
    show_error "Error: Please provide exactly one argument. $HELP_MESSAGE"
fi
# Validate that the argument is a number between 0 and 25
if ! [[ "$1" =~ ^[0-9]{2}$ ]] || [ "$1" -lt 0 ] || [ "$1" -gt 25 ]; then
    show_error "Error: $HELP_MESSAGE"
fi

# Run tasks
arg=$1
if [ "$arg" -eq 0 ]; then
    # Iterate over all files in folder inputs/
    for file in check/inputs/*; do
        if [[ -f "$file" ]]; then
            filename=$(basename ${file})
            run_program "$filename"
        fi
    done
else
    run_program "$arg"
fi

echo "Longest task execution time: $LONGEST"
