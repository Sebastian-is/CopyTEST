from bs4 import BeautifulSoup
import boto3
import datetime
import csv
import tempfile
import os

def obtener(bucket, ruta):
   s3 = boto3.client('s3')

   try:
      response = s3.get_object(Bucket=bucket, Key=ruta)
      contenido_html = response['Body'].read().decode('utf-8')
      return contenido_html
   except Exception as e:
      print(f"Error al obtener el archivo: {e}")
      return None


def main():
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    ruta = 'news/raw/contenido-'
    nombre_archivo = f'{fecha}.html' 
    ruta_archivo = f'{ruta}{nombre_archivo}'
    x = obtener('parcialbg' , ruta_archivo)

    generol = []
    titulol = []
    html = x
    soup = BeautifulSoup(html, 'html.parser')
    divs_article_details = soup.find_all('div', class_='article-details')
    for div in divs_article_details:
        titulo = div.find('a', class_= 'title page-link').text
        titulol.append(titulo)
    if div.find('div', class_='category-published') != None:
        genero = div.find('a').text
        generol.append(genero)
    else:
        genero = "encabezado"
        generol.append(genero)

    archivo_csv = 'datos.csv'
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as archivo:
        archivo_csv_temporal = archivo.name
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow(['Titulo', 'Genero'])
        for titu, gen in zip(titulol, generol):
            escritor_csv.writerow([titu, gen])

    print(f'Se ha creado el archivo CSV: {archivo_csv}')

    fecha_actual = datetime.datetime.now()
    bucket_name = "parcialcsv"
    dia = fecha_actual.day
    mes = fecha_actual.month
    anio = fecha_actual.year
    s3 = boto3.client('s3')
    pagina =  f'headlines/final/periodico/año={anio}/mes={mes}/{fecha}.csv'
    with open(archivo_csv_temporal, 'rb') as archivo:
        s3.put_object(Body=archivo , Bucket=bucket_name, Key=pagina)
    os.remove(archivo_csv_temporal)


main()
