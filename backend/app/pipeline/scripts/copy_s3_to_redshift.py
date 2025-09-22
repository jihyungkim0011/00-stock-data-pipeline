import configparser
import boto3
import os

def load_config(config_path='pipeline.conf'):
    """Loads configuration from an INI file."""
    parser = configparser.ConfigParser()
    # Correct the path to be relative to this script's location
    
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    try:
        parser.read(config_path)
        region_name = parser.get["redshift_copy","region_name"]
        workgroup_name = parser.get["redshift_copy",'workgroup_name']
        database_name = parser.get["redshift_copy",'database_name']
        db_user = parser.get["redshift_copy",'db_user']
        b_account_iam_role_arn = parser.get["redshift_copy",'b_account_iam_role_arn']
        a_account_iam_role_arn = parser.get["redshift_copy",'a_account_iam_role_arn']
        s3_bucket_name = parser.get["redshift_copy",'s3_bucket_name']
        s3_file_path = parser.get["redshift_copy",'s3_file_path']
        target_table = parser.get["redshift_copy",'target_table']
    
    except (FileNotFoundError, KeyError) as e:
        print(f"Error loading or parsing configuration: {e}")
        return

    return region_name, workgroup_name, database_name, db_user, b_account_iam_role_arn, a_account_iam_role_arn, s3_bucket_name, s3_file_path, target_table

def copy_s3_to_redshift():
    """
    Copies data from a CSV file in S3 to a Redshift table using
    configuration from pipeline.conf.
    """

    # Load configuration
    region_name, workgroup_name, database_name, db_user, b_account_iam_role_arn, a_account_iam_role_arn, s3_bucket_name, s3_file_path, target_table = load_config()

    if not all([region_name, workgroup_name, database_name, db_user, b_account_iam_role_arn, a_account_iam_role_arn, s3_bucket_name, s3_file_path, target_table]):
        print("Missing configuration values.")
        return

    # Create a Boto3 client for Redshift Data API
    client = boto3.client(
        'redshift-data', 
        region_name=region_name)

    # Construct the COPY command
    # Note: The f-string formatting for IAM_ROLE was incorrect. It should be a single string with two ARNs.
    copy_command = f"""
        COPY {target_table}
        FROM 's3://{s3_bucket_name}/{s3_file_path}'
        IAM_ROLE '{b_account_iam_role_arn},{a_account_iam_role_arn}'
        CSV
        IGNOREHEADER 1;
    """

    try:
        # Execute the COPY command
        print("Executing COPY command...")
        response = client.execute_statement(
            WorkgroupName=workgroup_name,
            Database=database_name,
            DbUser=db_user,
            Sql=copy_command
        )
        query_id = response['Id']
        print(f"Successfully submitted COPY command. Query ID: {query_id}")
        print("You can check the query status in the Redshift console.")

    except Exception as e:
        print(f"An error occurred while executing the COPY command: {e}")

if __name__ == "__main__":
    copy_s3_to_redshift()
