import requests
import datetime
import boto3

def get_html_content(url):
    response = requests.get(url)
    return response.text

def get_formatted_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def upload_to_s3(html_content, bucket_name, key):
    s3 = boto3.client('s3')
    s3.put_object(Body=html_content, Bucket=bucket_name, Key=key)

def main():
    url_add = "https://www.eltiempo.com/"
    html_content = get_html_content(url_add)
    fecha = get_formatted_date()
    pagina = f'news/raw/contenido-{fecha}.html'
    bucket_name = "parcial-html"

    upload_to_s3(html_content, bucket_name, pagina)

    print(f"Archivo '{pagina}' subido a '{bucket_name}'")

if __name__ == "__main__":
    main()
