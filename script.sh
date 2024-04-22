#!/bin/bash
# for airflow 
cd /home/marcus/workplace/Github/finance_project
PYTHON_PATH="/home/marcus/workplace/Github/finance_project/.venv/bin/python"

#source /home/marcus/workplace/Github/finance_project/.venv/bin/activate
echo "Python path is $PYTHON_PATH"
$PYTHON_PATH /home/marcus/workplace/Github/finance_project/stock_price.py "$(date)"
#deactivate