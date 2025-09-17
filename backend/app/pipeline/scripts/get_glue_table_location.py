import boto3
import configparser

parser = configparser.ConfigParser()

try: 
    # 아래 값들을 본인의 환경에 맞게 수정해주세요.
    db_name = parser.get("aws_glue", "database") # 생성한 Glue 데이터베이스 이름
    table_name = parser.get("aws_glue", "glue-table") # 생성한 Glue 테이블 이름
    region_name = parser.get("aws_glue", "region") # 사용 중인 AWS 리전

    client = boto3.client('glue', region_name=region_name)

    response = client.get_table(
        DatabaseName=db_name,
        Name=table_name
    )

    location = response['Table']['StorageDescriptor']['Location']
    print(f'Glue Table Location: {location}')

except Exception as e:
    print(f'An error occurred: {e}')
    print('Please check your database/table names and AWS credentials.')
