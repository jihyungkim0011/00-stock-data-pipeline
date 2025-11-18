import configparser
import boto3
import os
import time  # 대기 시간을 위해 추가
import sys

def load_config(config_path='pipeline.conf'):
    """설정 파일을 로드합니다."""
    parser = configparser.ConfigParser()
    
    if not os.path.exists(config_path):
        print(f"Error: 설정 파일이 없습니다 -> {config_path}")
        sys.exit(1) # 파일 없으면 바로 종료

    try:
        parser.read(config_path)
        config = parser["redshift_copy"] # 섹션 전체를 가져옴
        
        # 필요한 키값들이 다 있는지 확인
        required_keys = ["region_name", "workgroup_name", "database_name", "db_user", 
                         "b_account_iam_role_arn", "s3_bucket_name", "s3_file_path", "target_table"]
        
        # 설정값 딕셔너리 생성
        conf_data = {key: config.get(key) for key in required_keys}
        
        # AWS 자격증명도 함께 로드
        creds = parser["B_aws_credentials"]
        conf_data['aws_access_key'] = creds.get('access_key')
        conf_data['aws_secret_key'] = creds.get('secret_key')
        
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
    # 1. 설정 로드
    conf = load_config()

    # 2. Redshift Data API 클라이언트 생성
    client = boto3.client('redshift-data', 
                          region_name=conf['region_name'],
                          aws_access_key_id=conf['aws_access_key'],      # 여기!
                          aws_secret_access_key=conf['aws_secret_key'])

    # 3. COPY 명령어 생성 (수정됨)
    # - IAM_ROLE: B계정 역할 하나만 사용
    # - REGION: S3 리전을 명시 (여기서는 Redshift와 같다고 가정하고 설정값 사용)
    copy_command = f"""
        COPY {conf['target_table']}
        FROM 's3://{conf['s3_bucket_name']}/{conf['s3_file_path']}'
        IAM_ROLE '{conf['b_account_iam_role_arn']}'
        REGION '{conf['region_name']}'
        CSV
        IGNOREHEADER 1;
    """

    try:
        print("🚀 COPY 명령 전송 시작...")
        
        # 4. 실행 (비동기)
        response = client.execute_statement(
            WorkgroupName=conf['workgroup_name'],
            Database=conf['database_name'],
            DbUser=conf['db_user'], # Secrets Manager를 쓴다면 SecretArn으로 교체 권장
            Sql=copy_command
        )
        
        query_id = response['Id']
        
        # 5. 결과 대기 및 확인 (중요!)
        check_query_status(client, query_id)

    except Exception as e:
        print(f"🔥 스크립트 실행 중 에러 발생: {e}")

if __name__ == "__main__":
    copy_s3_to_redshift()