import requests
import datetime
import boto3


def obtener_contenido_pagina(url):
    response = requests.get(url)
    html_content = response.text
    return html_content


def subir_contenido_a_s3(html_content, bucket_name, key):
    s3 = boto3.client('s3')
    s3.put_object(Body=html_content, Bucket=bucket_name, Key=key)


def procesar_pagina_web():
    url_add = "https://www.eltiempo.com/"
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    pagina = f'news/raw/contenido-{fecha}.html'
    bucket_name = "parcial-html"

    html_content = obtener_contenido_pagina(url_add)
    subir_contenido_a_s3(html_content, bucket_name, pagina)

    print(f"Archivo '{pagina}' subido a '{bucket_name}'")


if __name__ == "__main__":
    procesar_pagina_web()
