# Finance Project with Telegram Bot

## 完成項目
1. Telegram Bot
2. API接口供Aitflow進行排程工作
3. 完整log記錄程式以利追蹤
4. Dockerfile
5. 心靈雞湯產生器

* [**機器人連結**](https://t.me/Marcus_First_Bot)

![image](./docs/telegram.jpg)

### airflow_dag.py
```python
from datetime import datetime, timedelta
import pytz

import requests
from airflow.decorators import dag
from airflow.operators.python import (
    BranchPythonOperator,
    PythonOperator
)
from airflow.operators.empty import EmptyOperator
from airflow.operators.email import EmailOperator
from setting import URL, EMAIL

def request_scraping(**context):
    execution = context['data_interval_end']
    date = execution.strftime("%Y-%d-%m")
    request_body = {'date':date}
    response = requests.get(
        f"{URL}/scraping/daily",
        params=request_body
    )

default_dags = {
    "owner": "MarcusLin",
    "depend_on_post": False,
    "start_date": datetime(
        2025,2,1,tzinfo=pytz.timezone("Asia/Taipei")
        ),
    "email": ['user@example.com'],
    "email_on_failure": False,
    "email_in_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=10)
}

def check_weekday(**context) -> str:
    execution_date = context['data_interval_end']
    day_of_week = execution_date.weekday()
    return "weekday" if day_of_week < 5 else "holiday"

def make_an_email(**context):
    execution_date = context['data_interval_end']
    task_instance = context['task_instance']
    if task_instance.xcom_pull(task_ids="check_weekday"):
        content = f"""
The scraping task for {execution_date} has been completed successfully.
Check in your maria database!!

Your Sincerely
Marcus.Lin
"""
    else:
        content = f"""
The day on {execution_date} is hoilday!
Please take a rest and exercising

Your Sincerely
Marcus.Lin
"""
    return content

@dag(
    dag_id="daily_stock_scraping",
    description="Daily scraping task",
    default_args=default_dags,
    schedule="0 17 * * *",
    catchup=False
)
def scraping():

    check = BranchPythonOperator(
        task_id='cheek_weekday',
        python_callable=check_weekday,
        provide_context = True,
        op_kwargs={"execute_date": "{{ data_interval_end }}"}
    )

    holiday = EmptyOperator(
        task_id="holiday",
        trigger_rule="none_failed_min_one_success"
    )

    weekday = EmptyOperator(
        task_id="weekday",
        trigger_rule="none_failed_min_one_success"
    )

    running_scraping = PythonOperator(
        task_id="Running_daily_scraping",
        python_callable=request_scraping,
        provide_context=True,
        trigger_rule='none_failed_min_one_success'
    )

    generate_email = PythonOperator(
        task_id='generate_email_content',
        python_callable=make_an_email,
        provide_context=True,
        trigger_rule='none_failed_min_one_success'
    )

    send_email = EmailOperator(
        task_id="send_email",
        to=EMAIL,
        subject="Daily Scraping Report",
        html_content="{{ task_instance.xcom_pull(task_ids='generate_email_content') }}",
        trigger_rule='none_failed_min_one_success'
    )

    check >> [weekday, holiday]
    weekday >> running_scraping >> generate_email >> send_email
    holiday >> generate_email >> send_email

scraping()
```

### 參考來源

[https://github.com/telunyang](https://github.com/telunyang)