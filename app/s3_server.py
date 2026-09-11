import os
import io
import boto3
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "utec")
DB_HOST = os.getenv("DB_HOST", "172.31.94.208")
DB_PORT = os.getenv("DB_PORT", "8004")
DB_NAME = os.getenv("DB_NAME", "cloud_eats_users")

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "cloud-eats-users-bucket-2026")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def export_users_to_s3():
    """Extrae los datos de MySQL y los sube en formato CSV a la capa /raw de S3."""
    engine = create_engine(DATABASE_URL)

    # 1. Extraer los datos con Pandas
    query = "SELECT id, name, email, phone, created_at FROM users;"
    df = pd.read_sql(query, con=engine)

    # 2. Generar archivo CSV en memoria RAM
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    # 3. Construir clave/nombre del archivo con fecha
    date_str = datetime.now().strftime("%Y-%m-%d")
    s3_key = f"raw/users_{date_str}.csv"

    # 4. Subir a S3 usando Boto3
    s3_client = boto3.client("s3", region_name=AWS_REGION)
    s3_client.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=s3_key,
        Body=csv_buffer.getvalue(),
        ContentType="text/csv"
    )

    return f"s3://{S3_BUCKET_NAME}/{s3_key}"