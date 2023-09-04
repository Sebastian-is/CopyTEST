import requests
import datetime
import boto3


def main():
    url_add = "https://www.eltiempo.com/"
    response = requests.get(url_add)
    html_content = response.text
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    pagina = f'news/raw/contenido-{fecha}.html'

    bucket_name = "parcial-html"

    s3 = boto3.client('s3')
    s3.put_object(Body=html_content, Bucket=bucket_name, Key=pagina)

    print(f"Archivo '{pagina}' subido a '{bucket_name}'")


if name == "main":
    main()
