#!/bin/bash

# Group members: Lex Albrandt albrandt

VAL1=-1                     # beginning loop value
VAL2=-1                     # end loop value
VERBOSE=0                   # Verbose mode

# Shows help function
function show_help()
{
    echo "./run_test.bash [-h] [-b <begin>] [-e <end>] [-v]"
    echo "Today's date is $(date)"
    exit 0
}

while getopts "hb:e:v" OPT
do
    case "${OPT}" in
        # Show help function
        h)
            show_help
            ;;
        # Set beginning loop value
        b)
            VAL1=${OPTARG}
            ;;
        # Set end loop value
        e)
            VAL2=${OPTARG}
            ;;
        # Enable verbose mode
        v)
            VERBOSE=1
            ;;
        # Default
        *)
            show_help
            ;;
    esac
done

# If neither -e or -b values are given, show help
#if [ $VAL1 -eq -1 ] && [ $VAL2 -eq -1 ]
#then
#    show_help
#fi

# shows help if no value given
if [ $VAL2 -eq -1 ]
then
    VAL2=10                         # Set to default 10
fi

# shows help if no value given
if [ $VAL2 -eq -1 ]
then
    VAL1=1                         # Set to default 1
fi

# show help if end is greater than beginning
if [ $VAL1 -gt $VAL2 ]
then
    show_help
fi
        
for VALUE in $(seq $VAL1 $VAL2) 
do
    ./hydra $VALUE
    EXIT_VAL=$?

    if [ $EXIT_VAL -eq 0 ]
    then
        echo "$VALUE was successful"
    elif [ $VERBOSE -eq 1 ]
    then
        echo "$VALUE returned $EXIT_VAL"
    fi
done