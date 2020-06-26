#!/bin/bash
export color_prompt=yes
cd 1lims-automation;
export PYTHONPATH='$PYTHONPATH:/1lims-automation';
export LOGURU_LEVEL='DEBUG';
xvfb-run -a nosetests -vs --nologcapture --tc-file=config.ini ui_testing/testcases/basic_tests/test04_testunits.py:TestUnitsTestCases
