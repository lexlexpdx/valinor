#/!bin/bash

UB=500
TEST_DIR=test-files
BASE_FILE=base-file.hex

if [ ! -d ${TEST_DIR} ]
then
    mkdir ${TEST_DIR}
    echo "directory created"
else
    rm -f ${TEST_DIR}/R*.hex
    echo "directory cleared"
fi

head -c 500K < /dev/urandom             \
     | xxd                              \
     | cut -d ' ' -f2,3,4,5,6,7,8,9     \
     | tr -d ' '                        \
     > ${BASE_FILE}
echo "base file created"

for (( VAL=0 ; VAL<=${UB} ; VAL++ ))
do
    cp ${BASE_FILE} ${TEST_DIR}/R${RANDOM}.hex
done
echo "${UB} copy files made"

sed -z -e 's/a/A/1000' ${BASE_FILE} > ${TEST_DIR}/R${RANDOM}.hex
echo "diff file made"

for FILE in ${TEST_DIR}/R*.hex
do
    touch -t 196907202256.15 ${FILE}
done
COUNT=$(ls -1 ${TEST_DIR} | wc -l)

echo "timestamps set on ${COUNT} files"
