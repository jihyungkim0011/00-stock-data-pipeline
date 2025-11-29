import configparser
import boto3
import os
import time
import sys
from typing import Dict, List

def load_config(config_path='pipeline.conf'):
    """설정 파일을 로드합니다."""
    parser = configparser.ConfigParser()
    
    if not os.path.exists(config_path):
        print(f"Error: 설정 파일이 없습니다 -> {config_path}")
        sys.exit(1) # 파일 없으면 바로 종료

    try:
        parser.read(config_path)
        config = parser["redshift_copy"] 
        
        conf_data = {
            "region_name": config.get("region_name"),
            "workgroup_name": config.get("workgroup_name"),
            "database_name": config.get("database_name"),
            "b_account_iam_role_arn": config.get("b_account_iam_role_arn"),
            "b_account_secret_arn": config.get("b_account_secret_arn"),
            "s3_bucket_name": config.get("s3_bucket_name")
        }

        # AWS 자격증명도 함께 로드
        creds = parser["B_aws_credentials"]
        conf_data['aws_access_key'] = creds.get('access_key')
        conf_data['aws_secret_key'] = creds.get('secret_key')
        
        # 테이블 목록 설정 (동적 섹션) 로드
        table_configs: List[Dict[str, str]] = []
        # 'table_1', 'table_2' 와 같은 패턴의 섹션을 찾습니다.
        table_sections = [s for s in parser.sections() if s.startswith('table_')]
        
        if not table_sections:
            print("Error: 설정 파일에서 'table_'로 시작하는 테이블 섹션을 찾을 수 없습니다.")
            sys.exit(1)
            
        for section_name in table_sections:
            table_conf = parser[section_name]
            # 개별 테이블에 필요한 키 확인
            required_keys = ["s3_file_path", "target_table"]
            
            # 테이블 설정 딕셔너리 생성
            temp_conf = {key: table_conf.get(key) for key in required_keys}
            
            # 파싱된 테이블 설정에 추가적인 Redshift COPY 옵션 (예: FORMAT, IGNOREHEADER)도 포함 가능
            temp_conf['format'] = table_conf.get('format', 'CSV') # 기본값 CSV
            temp_conf['ignoreheader'] = table_conf.get('ignoreheader', '1') # 기본값 1
            
            table_configs.append(temp_conf)
            
        conf_data['table_configs'] = table_configs
        return conf_data
    
    except Exception as e:
        print(f"설정 파일 읽기 실패: {e}")
        sys.exit(1)

def check_query_status(client, query_id):
    """쿼리가 끝날 때까지 기다리고 결과를 확인합니다."""
    print(f"🔄 쿼리 실행 중... (ID: {query_id})")
    
    while True:
        response = client.describe_statement(Id=query_id)
        status = response['Status']
        
        if status == 'FINISHED':
            print("✅ 성공! (데이터 적재 완료)")
            return True
        elif status == 'FAILED':
            print(f"❌ 실패! 에러 메시지: {response['Error']}")
            return False
        elif status == 'ABORTED':
            print("🚫 취소됨.")
            return False
        
        # 아직 실행 중이면 2초 쉬고 다시 확인
        time.sleep(2)

def copy_s3_to_redshift():
    # 설정 로드
    success_count = 0
    fail_count = 0
    conf = load_config()

    # Redshift Data API 클라이언트 생성
    client = boto3.client(
        'redshift-data', 
        region_name=conf['region_name'],
        aws_access_key_id=conf['aws_access_key'],
        aws_secret_access_key=conf['aws_secret_key'],
    )
    
    # 각 테이블에 대해 COPY 명령 실행
    for table_conf in conf['table_configs']:
        target_table = table_conf['target_table']
        s3_path = table_conf['s3_file_path']
        file_format = table_conf['format']
        ignore_header = table_conf['ignoreheader']
        
        print("\n=======================================================")
        print(f"🚀 {target_table} 테이블로 데이터 적재 시작...")
        print(f"📦 S3 경로: s3://{conf['s3_bucket_name']}/{s3_path}")
        
        # COPY 명령어 생성 (테이블별 옵션 적용)
        copy_command = f"""
            COPY {target_table}
            FROM 's3://{conf['s3_bucket_name']}/{s3_path}'
            IAM_ROLE '{conf['b_account_iam_role_arn']}'
            REGION '{conf['region_name']}'
            {file_format}
            IGNOREHEADER {ignore_header}
            TIMEFORMAT 'auto';
        """
        
        try:
            # 5. 실행 (비동기)
            response = client.execute_statement(
                WorkgroupName=conf['workgroup_name'],    
                Database=conf['database_name'],
                SecretArn=conf['b_account_secret_arn'],
                Sql=copy_command
            )
            query_id = response['Id']
            
            if check_query_status(client, query_id):
                success_count += 1
            else:
                fail_count += 1

        except Exception as e:
            print(f"🔥 {target_table} 테이블 작업 중 에러 발생: {e}")
            fail_count += 1
    
    # 6. 최종 요약 출력
    print("\n=======================================================")
    print(f"✨ 모든 테이블 적재 작업 완료 (성공: {success_count}, 실패: {fail_count})")

if __name__ == "__main__":
    copy_s3_to_redshift()