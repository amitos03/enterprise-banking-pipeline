import os
import json
import csv
import random
import uuid
from datetime import datetime, timedelta
import boto3
from dotenv import load_dotenv
from faker import Faker

# 1. Initialize environment and tools
load_dotenv()
fake = Faker('en_IN') # Using Indian locale for realistic names and cities

# S3 Configuration
BUCKET_NAME = os.getenv('BUCKET_NAME')
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

# Shared Account IDs to ensure we can join this data later in Snowflake
SHARED_ACCOUNT_IDS = [f"ACCT-{random.randint(1000, 9999)}" for _ in range(50)]

# ==========================================
# GENERATOR 1: OLTP TRANSACTIONS (CSV)
# ==========================================
def generate_oltp_data(num_records=500):
    filename = "oltp_transactions.csv"
    print(f"Generating {num_records} OLTP transactions...")
    
  # Change this:
with open(filename, mode='w', newline='') as file:

# To this:
with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Standard Relational Headers
        writer.writerow(['transaction_id', 'account_id', 'amount', 'currency', 'txn_timestamp', 'merchant', 'status'])
        
        for _ in range(num_records):
            writer.writerow([
                str(uuid.uuid4()),
                random.choice(SHARED_ACCOUNT_IDS),
                round(random.uniform(10.0, 50000.0), 2),
                'INR',
                fake.date_time_between(start_date='-30d', end_date='now').isoformat(),
                fake.company(),
                random.choices(['CLEARED', 'PENDING', 'FAILED'], weights=[85, 10, 5])[0]
            ])
    return filename

# ==========================================
# GENERATOR 2: SALESFORCE CRM (NESTED JSON)
# ==========================================
def generate_salesforce_crm_data():
    filename = "salesforce_crm.json"
    print("Generating Salesforce CRM profiles...")
    
    crm_data = []
    for account_id in SHARED_ACCOUNT_IDS:
        profile = {
            "sf_contact_id": f"SF-{uuid.uuid4().hex[:8]}",
            "linked_account_id": account_id,
            "personal_details": {
                "full_name": fake.name(),
                "email": fake.company_email(),
                "phone": fake.phone_number(),
                "address": {
                    "city": fake.city(),
                    "state": fake.state(),
                    "pin_code": fake.postcode()
                }
            },
            "risk_score": random.randint(300, 850),
            # Array of nested JSON objects (simulating support tickets)
            "support_cases": [
                {
                    "case_id": f"CASE-{random.randint(100,999)}",
                    "issue_type": random.choice(["Login Issue", "Fraud Report", "Card Replacement"]),
                    "status": random.choice(["Open", "Closed"])
                } for _ in range(random.randint(0, 3))
            ]
        }
        crm_data.append(profile)
        
    with open(filename, "w") as file:
        json.dump(crm_data, file, indent=4)
    return filename

# ==========================================
# GENERATOR 3: KYC VENDOR API (TEXT / UNSTRUCTURED)
# ==========================================
def generate_kyc_documents():
    print("Generating KYC OCR text dumps...")
    filenames = []
    # Generate 5 random KYC documents
    for _ in range(5):
        doc_id = f"KYC-DOC-{uuid.uuid4().hex[:6]}"
        filename = f"{doc_id}.txt"
        with open(filename, "w") as file:
            file.write(f"DOCUMENT ID: {doc_id}\n")
            file.write(f"EXTRACTION DATE: {datetime.now().isoformat()}\n")
            file.write(f"ENTITY DETECTED: {fake.name()}\n")
            file.write("CONFIDENCE SCORE: 98%\n")
            file.write("RAW OCR TEXT: IDENTIFICATION CARD GOVT OF INDIA DO NOT REPLICATE...\n")
        filenames.append(filename)
    return filenames

# ==========================================
# UPLOAD ENGINE (WITH KMS ENCRYPTION)
# ==========================================
def upload_to_s3(filename, s3_folder_prefix):
    s3_key = f"{s3_folder_prefix}/{filename}"
    print(f"Uploading {filename} to s3://{BUCKET_NAME}/{s3_key} (Encrypted)...")
    try:
        # ExtraArgs enforces AWS KMS Server-Side Encryption
        s3_client.upload_file(
            filename, 
            BUCKET_NAME, 
            s3_key,
            ExtraArgs={'ServerSideEncryption': 'aws:kms'}
        )
    except Exception as e:
        print(f"❌ Upload failed: {e}")

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    print("🚀 Starting Enterprise Data Simulation Engine...")
    
    # 1. Generate Data
    csv_file = generate_oltp_data()
    json_file = generate_salesforce_crm_data()
    txt_files = generate_kyc_documents()
    
    # 2. Upload to Partitioned S3 Folders
    upload_to_s3(csv_file, "raw/oltp")
    upload_to_s3(json_file, "raw/salesforce")
    for txt in txt_files:
        upload_to_s3(txt, "raw/kyc_docs")
        
    print("✅ All multi-source data generated and securely uploaded to AWS S3.")