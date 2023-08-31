import os
import boto3
from bs4 import BeautifulSoup
import json

def lambda_handler(event, context):
    # Obtiene el nombre del archivo más reciente
    bucket_name = os.environ['S3_BUCKET']
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key='latest-file.json')
    latest_filename_str = response['Body'].read().decode('utf-8')
    latest_filename = json.loads(latest_filename_str)['filename']

    # Accede al contenido del archivo HTML más reciente
    response = s3.get_object(Bucket=bucket_name, Key=latest_filename)
    html_content = response['Body'].read().decode('utf-8')

    # Procesa el contenido HTML usando BeautifulSoup u otras herramientas
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extrae la información que necesitas (categoría, titular, enlace)
    category_div = soup.find('div', class_='category-published')
    category_a = category_div.find('a')
    category = category_a.text.strip()

    headline = ''
    if soup.find('h1'):
        headline = soup.find('h1').text.strip()
    elif soup.find('h2'):
        headline = soup.find('h2').text.strip()

    link = ''
    if headline:
        link = category_a['href']

    # Crea el contenido del CSV
    csv_content = f'{category},{headline},{link}'

    # Sube el archivo CSV a S3 en la ruta "headlines/final/"
    csv_key = 'headlines/final/' + latest_filename.replace("news/raw/contenido-", "").replace(".html", ".csv")
    s3.put_object(Bucket=bucket_name, Key=csv_key, Body=csv_content.encode('utf-8'))
