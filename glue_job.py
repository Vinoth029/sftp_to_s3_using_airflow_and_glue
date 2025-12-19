import boto3
import json
import paramiko
import os
from datetime import datetime

# ------------------------------
# CONFIG
# ------------------------------
SECRET_NAME = "onprem_sftp_secret"
REGION = "ap-south-1"
S3_BUCKET = "branch-analytics-raw"
DATASET = "branch_transactions"
TMP_DIR = "/tmp"

# ------------------------------
# CLIENTS
# ------------------------------
secrets_client = boto3.client("secretsmanager", region_name=REGION)
s3_client = boto3.client("s3")

# ------------------------------
# LOAD SFTP CREDENTIALS
# ------------------------------
secret = json.loads(
    secrets_client.get_secret_value(SecretId=SECRET_NAME)["SecretString"]
)

HOST = secret["host"]
PORT = secret.get("port", 22)
USERNAME = secret["username"]
PASSWORD = secret["password"]
REMOTE_PATH = secret["remote_path"]

# ------------------------------
# CONNECT TO SFTP
# ------------------------------
transport = paramiko.Transport((HOST, PORT))
transport.connect(username=USERNAME, password=PASSWORD)
sftp = paramiko.SFTPClient.from_transport(transport)

# ------------------------------
# LIST FILES
# ------------------------------
files = sftp.listdir(REMOTE_PATH)

if not files:
    print("No files found in SFTP directory")
    exit(0)

load_date = datetime.now().strftime("%Y-%m-%d")

# ------------------------------
# DOWNLOAD & UPLOAD TO S3
# ------------------------------
for file_name in files:
    remote_file = f"{REMOTE_PATH}/{file_name}"
    local_file = f"{TMP_DIR}/{file_name}"

    print(f"Downloading {remote_file}")
    sftp.get(remote_file, local_file)

    s3_key = (
        f"source=sftp/dataset={DATASET}/"
        f"load_date={load_date}/"
        f"{file_name}"
    )

    print(f"Uploading to s3://{S3_BUCKET}/{s3_key}")
    s3_client.upload_file(local_file, S3_BUCKET, s3_key)

    os.remove(local_file)

# ------------------------------
# CLEANUP
# ------------------------------
sftp.close()
transport.close()

print("SFTP ingestion completed successfully")
