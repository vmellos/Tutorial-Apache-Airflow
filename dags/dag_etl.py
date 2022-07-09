import pendulum
import requests
import json
from datetime import timedelta

import pandas as pd

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

TIMEZONE = 'America/Sao_Paulo'


def _get_dataframe() -> pd.DataFrame:
    url = 'https://servicodados.ibge.gov.br/api/v3/agregados?classificacao=1'
    r = requests.get(url)
    agregados = r.json()[0]['agregados']
    data = json.dumps(agregados)
    return pd.read_json(data)


def _read_file(**kwargs):
    ti = kwargs['ti']

    df = _get_dataframe()
    ti.xcom_push(key='dataframe', value=df)


def _validate_file(**kwargs):
    ti = kwargs['ti']
    df = ti.xcom_pull(key='dataframe')

    df_filtered_10 = df[df['nome'].str.contains('10')]

    ti.xcom_push(key='dataframe', value=df_filtered_10)


def _create_file(**kwargs):
    ti = kwargs['ti']
    df = ti.xcom_pull(key='dataframe')

    df = df.reset_index(drop=True)

    df.to_csv('new_loaded.csv', header=False, sep=',', index=False, encoding="utf-8")


with DAG(
        'tutorial_primeira_etl',
        default_args={
            'depends_on_past': False,
        },
        description='Primeira ETL',
        schedule_interval=timedelta(days=1),
        start_date=pendulum.today(TIMEZONE).add(days=-1),
        catchup=False,
) as dag:
    task_start = DummyOperator(task_id='start')

    task_read_file = PythonOperator(
        task_id='task_read_file',
        python_callable=_read_file,
        dag=dag
    )

    task_validate_file = PythonOperator(
        task_id='task_validate_file',
        python_callable=_validate_file,
        dag=dag
    )

    task_create_file = PythonOperator(
        task_id='task_create_file',
        python_callable=_create_file,
        dag=dag
    )

    task_end = DummyOperator(task_id='end')

    task_start >> task_read_file >> task_validate_file >> task_create_file >> task_end
