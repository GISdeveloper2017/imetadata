!/bin/bash
pytest test -s --alluredir report/src
allure generate report/src -o report/rpt --clean
