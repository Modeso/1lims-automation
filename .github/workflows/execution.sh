#!/bin/bash

EXECUTION_FILES=(
      ui_testing/testcases/header_tests/test011_rolesandpermissions.py
      ui_testing/testcases/header_tests/test008_company_profile.py
      )

NODE_TOTAL=$1;
NODE_INDEX=$2;
TEST_REG=$3;
RUN_REF=$4;
RUN_ID=$5;
RUN_NUMBER=$6;
WORK_DIR=$7;

echo 'NODE_TOTAL: ' $NODE_INDEX;
echo 'NODE_INDEX: ' $NODE_TOTAL;
echo 'TEST_REG: ' $TEST_REG;
echo 'RUN_REF: ' $RUN_REF;
echo 'RUN_ID: ' $RUN_ID;
echo 'RUN_NUMBER: ' $RUN_NUMBER;
echo 'WORK_DIR: ' $WORK_DIR;


for TEST_FILE in "${EXECUTION_FILES[@]}"
 do
   docker container run -t --shm-size=2g -v $WORK_DIR:/1lims-automation -e "PYTHONPATH='$PYTHONPATH:/1lims-automation" -w /1lims-automation 0xislamtaha/seleniumchromenose:83 bash -c "NODE_TOTAL=$NODE_TOTAL NODE_INDEX=$NODE_INDEX nosetests -vs --nologcapture --with-reportportal --rp-config-file rp.ini --rp-launch-description=$RUN_REF-$RUN_ID-$RUN_NUMBER --tc-file=config.ini --tc=browser.headless:True --with-flaky --force-flaky --max-runs=3 --min-passes=1 --with-parallel -A 'not series' -m '$TEST_REG' $TEST_FILE"
 done