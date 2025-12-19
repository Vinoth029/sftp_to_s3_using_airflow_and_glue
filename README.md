# 📌 On-Prem SFTP to Amazon S3 (Raw Zone) using Airflow & AWS Glue

## 📖 Overview

This project implements a **production-grade data ingestion pipeline** that transfers files from an **on-premise SFTP server** into **Amazon S3 (Raw Zone)**.

The pipeline is **orchestrated using Apache Airflow** and uses an **AWS Glue Python Shell job** to securely connect to the on-prem SFTP server using credentials stored in **AWS Secrets Manager**.

This design follows **enterprise data lake best practices**, ensuring security, reliability, and auditability.

---

## 🏗 Architecture

**End-to-End Flow:**

1. Apache Airflow triggers the AWS Glue job on a schedule
2. AWS Glue retrieves SFTP credentials from AWS Secrets Manager
3. Glue connects to the on-prem SFTP server via VPN / Direct Connect
4. Files are downloaded from the SFTP directory
5. Raw files are uploaded unchanged to Amazon S3
6. Airflow monitors execution and retries on failure

**Design Principles:**
- Secure credential management
- Cost-optimized ingestion
- Raw zone immutability
- Retry and failure handling
- Easy replay and audit support

---

## 🧰 Technology Stack

| Component | Purpose |
|--------|--------|
| Apache Airflow | Workflow orchestration |
| AWS Glue (Python Shell) | SFTP ingestion |
| AWS Secrets Manager | Secure SFTP credentials |
| Amazon S3 | Raw data storage |
| AWS IAM | Access control |
| CloudWatch | Logging & monitoring |

---

## 📁 S3 Raw Data Layout

```text
s3://branch-analytics-raw/
└── source=sftp/
    └── dataset=branch_transactions/
        └── load_date=YYYY-MM-DD/
            └── <original_filename>
