from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_engineering_team',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'enterprise_banking_pipeline',
    default_args=default_args,
    description='End-to-end ELT for multi-source banking data',
    schedule_interval='0 0 * * *',
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    # Task 1: Trigger the Python extraction script
    extract_and_load_to_s3 = BashOperator(
        task_id='extract_multi_source_data',
        bash_command='echo "Simulating Python extraction to AWS S3..."'
    )

    # Task 2: Pause to allow Snowpipe serverless compute to ingest the files
    wait_for_snowpipe = BashOperator(
        task_id='wait_for_snowpipe_ingestion',
        bash_command='sleep 60'
    )

    # Task 3: The real dbt Cloud Operator
    run_dbt_transformations = DbtCloudRunJobOperator(
        task_id='run_dbt_staging_and_marts',
        dbt_cloud_conn_id='dbt_cloud_default',
        job_id=12345, 
        check_interval=20,
        timeout=300
    )

    extract_and_load_to_s3 >> wait_for_snowpipe >> run_dbt_transformations