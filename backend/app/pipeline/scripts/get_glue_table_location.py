import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

def run_glue_etl_job(source_s3_path, redshift_table, redshift_connection, redshift_temp_dir, drop_columns=None):
    """
    AWS Glue ETL 작업을 실행하여 S3 데이터를 Redshift로 복사하는 함수.

    Args:
        source_s3_path (str): S3에 있는 소스 데이터 경로.
        redshift_table (str): 데이터를 로드할 Redshift 테이블 이름.
        redshift_connection (str): Redshift 연결을 위한 Glue Connection 이름.
        redshift_temp_dir (str): Redshift가 데이터를 로드할 때 사용할 임시 S3 경로.
        drop_columns (list, optional): 삭제할 컬럼 이름 리스트. 기본값은 None.
    """
    # Glue 작업 초기화
    args = getResolvedOptions(sys.argv, ["JOB_NAME"])
    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    job = Job(glueContext)
    job.init(args["JOB_NAME"], args)

    # 1. 데이터 소스 (S3)에서 데이터 읽기
    source_data = glueContext.create_dynamic_frame.from_options(
        connection_type="s3",
        connection_options={"paths": [source_s3_path]},
        format="csv",
        transformation_ctx="source_data",
    )

    # 2. 데이터 변환 (컬럼 삭제)
    if drop_columns:
        transformed_data = DropFields.apply(
            frame=source_data,
            paths=drop_columns,
            transformation_ctx="transformed_data",
        )
    else:
        transformed_data = source_data

    # 3. 변환된 데이터를 Redshift Serverless에 쓰기
    glueContext.write_dynamic_frame.from_options(
        frame=transformed_data,
        connection_type="redshift",
        connection_options={
            "redshiftTmpDir": redshift_temp_dir,
            "useConnectionProperties": "true",
            "dbtable": redshift_table,
            "connectionName": redshift_connection,
        },
        transformation_ctx="destination_data",
    )

    # 작업 완료
    job.commit()


# 함수 호출 예시
run_glue_etl_job(
    source_s3_path="s3://your-s3-bucket/your-data-folder/",
    redshift_table="your_redshift_table",
    redshift_connection="your_glue_redshift_connection",
    redshift_temp_dir="s3://your-temp-bucket/redshift-temp/",
    drop_columns=["unnecessary_column"] # 필요에 따라 컬럼을 지정
)