import boto3
import requests
import datetime
import os
import json

print("Starting function execution...")
# URL de la página a descargar
url = 'https://www.eltiempo.com'

# Obtiene la fecha actual
current_date = datetime.datetime.now().strftime('%Y-%m-%d')

# Nombre del archivo en S3
s3_filename = f'news/raw/contenido-{current_date}.html'

# Descarga la página
response = requests.get(url)
content = response.text

# Sube el contenido a S3
bucket_name = os.environ['S3_BUCKET']  # Nombre del bucket de S3
s3 = boto3.client('s3')
s3.put_object(Body=content, Bucket=bucket_name, Key=s3_filename)

latest_filename = {'filename': s3_filename}
latest_filename_str = json.dumps(latest_filename)
s3.put_object(Body=latest_filename_str, Bucket=bucket_name, Key='latest-file.json')

