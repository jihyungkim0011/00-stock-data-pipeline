import pymysql
import csv
import boto3
import configparser

# MySQL 데이터베이스 연결
parser = configparser.ConfigParser()
parser.read("pipeline.conf")
host = parser.get("mysql_config", "hostname")
port = parser.get("mysql_config", "port")
username = parser.get("mysql_config", "username")
dbname = parser.get("mysql_config", "database")
password = parser.get("mysql_config", "password")

conn = pymysql.connect(
    user= username,
    password= password,
    db=dbname,
    port=int(port),
)

if conn is None:
    print("Error connecting to the MySQL database")
else:
    print("Connected to the MySQL database successfully")

# MySQL 쿼리 실행 및 결과를 CSV 파일로 저장
m_query = "SELECT * FROM Orders"
local_filename = "orders_extract.csv"

m_cursor = conn.cursor()
m_cursor.execute(m_query)
results = m_cursor.fetchall()

with open(local_filename, "w") as fp:
    csv_writer = csv.writer(fp, delimiter='|')
    csv_writer.writerows(results)
fp.close()
m_cursor.close()
conn.close()

# aws boto 크레딧 로드
parser = configparser.ConfigParser()
parser.read("pipeline.conf")
access_key = parser.get("aws_boto_crecdentials", "access_key")
secret_key = parser.get("aws_boto_crecdentials", "secret_key")
bucket_name = parser.get("aws_boto_crecdentials", "bucket_name")

s3 = boto3.client(
    "s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
)

# S3에 파일 업로드
s3_file = local_filename
s3.upload_file(
    Filename=local_filename,
    Bucket=bucket_name,
    Key=s3_file,
)

