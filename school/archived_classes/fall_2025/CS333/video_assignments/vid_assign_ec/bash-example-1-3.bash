#!/bin/bash

TEST_DIR=test-files
SHA_FILE=sha_file.txt

if [ -e ${SHA_FILE} ]
then
    rm -f ${SHA_FILE}
fi

touch ${SHA_FILE}
for FILE in ${TEST_DIR}/R*.hex
do
    sha256sum ${FILE} >> ${SHA_FILE}
done

FOUND_SHA=$(cut -d ' ' -f 1 ${SHA_FILE} | sort | uniq -c | sort -n | head -1 | awk '{print $2;}')

grep ${FOUND_SHA} ${SHA_FILE}
