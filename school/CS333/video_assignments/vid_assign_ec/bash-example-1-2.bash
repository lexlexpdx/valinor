#!/bin/bash

BASE_FILE=base-file.hex
TEST_DIR=test-files

for FILE in ${TEST_DIR}/R*.hex
do
    diff -q ${BASE_FILE} ${FILE} 1> /dev/null 2> /dev/null
    if [ $? -eq 1 ]
    then
        echo "Congratulations! The files ${BASE_FILE} and ${FILE} differ."
        diff ${BASE_FILE} ${FILE}
        break
    fi
done

for FILE in ${TEST_DIR}/R*.hex
do
    cmp ${BASE_FILE} ${FILE} 1> /dev/null 2> /dev/null
    if [ $? -eq 1 ]
    then
        echo -e "You have found it!\n\tThe files ${BASE_FILE} and ${FILE} compare different."
        cmp ${BASE_FILE} ${FILE}
        break
    fi
done