# CDC방식 : 실시간 변화에 대응 가능. 데이터 누락을 최소화할 수 있다. 운영난이도는 높음

from pymysqlreplication import BinLogStreamReader
from pymysqlreplication import row_event
import configparser
import csv
import boto3

# MySQL 데이터베이스 연결
parser = configparser.ConfigParser()
parser.read("pipeline.conf")
hostname = parser.get("mysql_config", "hostname")
port = parser.get("mysql_config", "port")
username = parser.get("mysql_config", "username")
password = parser.get("mysql_config", "password")

mysql_settings = {
    "host": hostname,
    "port": int(port),
    "user": username,
    "passwd": password,
}

b_stream = BinLogStreamReader(
    connection_settings=mysql_settings,
    server_id=100,
    only_events=[row_event.WriteRowsEvent, 
                 row_event.UpdateRowsEvent, 
                 row_event.DeleteRowsEvent],
)

order_events = []

for binlogevent in b_stream:
    for row in binlogevent.rows:
        event = {}
        if isinstance(binlogevent, row_event.DeleteRowsEvent):
            event["action"] = "delete"
            event.update(row["values"].items())
        elif isinstance(binlogevent, row_event.UpdateRowsEvent):
            event["action"] = "update"
            event.update(row["after_values"].items())
        elif isinstance(binlogevent, row_event.WriteRowsEvent):
            event["action"] = "insert"
            event.update(row["values"].items())
        
        order_events.append(event)

b_stream.close()

keys = order_events[0].keys()
local_filename = "orders_binlog_extract.csv"

with open(local_filename, "w", newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys, delimiter='|')
    dict_writer.writerows(order_events)


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

