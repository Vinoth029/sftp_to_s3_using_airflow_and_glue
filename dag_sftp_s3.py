from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import AwsGlueJobOperator
from datetime import datetime

with DAG(
    dag_id="onprem_sftp_to_s3_raw",
    start_date=datetime(2025, 1, 1),
    schedule_interval="0 9 * * *",
    catchup=False,
    tags=["sftp", "glue", "raw"]
) as dag:

    trigger_sftp_glue = AwsGlueJobOperator(
        task_id="run_sftp_ingestion",
        job_name="onprem_sftp_raw_ingestion",
        region_name="ap-south-1",
        aws_conn_id="aws_default",
        retries=2
    )

    trigger_sftp_glue
