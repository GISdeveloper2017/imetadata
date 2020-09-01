!/bin/bash
rm report/src/*.*
pytest test --alluredir report/src
allure generate report/src -o report/rpt --clean