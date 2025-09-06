import configparser
import boto3
import os

def load_aws_boto_credentials(file_path="pipeline.conf"):
    """
    설정 파일에서 AWS 자격 증명을 로드하여 S3 클라이언트 객체를 반환합니다.
    """
    parser = configparser.ConfigParser()
    try:
        parser.read(file_path)
        access_key = parser.get("aws_boto_credentials", "access_key")
        secret_key = parser.get("aws_boto_credentials", "secret_key")
        bucket_name = parser.get("aws_boto_credentials", "bucket_name")

        s3_client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        return s3_client, bucket_name

    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"설정 파일에서 AWS 자격 증명 정보를 찾을 수 없습니다: {e}")
        return None, None
    except Exception as e:
        print(f"설정 파일을 읽는 중 오류가 발생했습니다: {e}")
        return None, None

def upload_file_to_s3(s3_client, bucket_name, local_file_path, s3_key):
    """
    지정된 로컬 파일을 S3 버킷에 업로드합니다.
    """
    try:
        s3_client.upload_file(
            Filename=local_file_path,
            Bucket=bucket_name,
            Key=s3_key,
        )
        print(f"'{local_file_path}' 파일이 S3의 '{s3_key}' 경로에 성공적으로 업로드되었습니다.")
        return True
    except Exception as e:
        print(f"'{local_file_path}' 파일 업로드 중 오류가 발생했습니다: {e}")
        return False

def upload_all_csv_in_folder(s3_client, bucket_name, source_folder, s3_prefix=""):
    """
    지정된 로컬 폴더 내의 모든 .csv 파일을 S3에 업로드합니다.
    """
    if not os.path.isdir(source_folder):
        print(f"오류: '{source_folder}' 폴더를 찾을 수 없습니다.")
        return

    print(f"'{source_folder}' 폴더에서 .csv 파일을 찾고 있습니다...")
    
    # os.walk를 사용하여 하위 폴더까지 탐색
    for root, dirs, files in os.walk(source_folder):
        for filename in files:
            if filename.endswith(".csv"):
                local_file_path = os.path.join(root, filename)
                # S3 키 경로 생성 (로컬 폴더 구조를 유지)
                relative_path = os.path.relpath(local_file_path, start=source_folder)
                s3_key = os.path.join(s3_prefix, relative_path).replace("\\", "/")

                upload_file_to_s3(s3_client, bucket_name, local_file_path, s3_key)

if __name__ == "__main__":
    SOURCE_FOLDER = "data/"  # 업로드할 로컬 폴더 경로
    S3_PREFIX = "stock_csv/" # S3 버킷 내의 원하는 경로 (폴더)

    # 1. AWS 자격 증명 및 S3 클라이언트 로드
    s3, bucket = load_aws_boto_credentials()
    
    if s3 and bucket:
        # 2. 'data' 폴더 내의 모든 CSV 파일 S3에 업로드
        upload_all_csv_in_folder(s3, bucket, SOURCE_FOLDER, S3_PREFIX)
    
    print("모든 작업이 완료되었습니다.")