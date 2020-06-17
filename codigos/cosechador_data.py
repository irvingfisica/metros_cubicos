import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import json
import time

enlaces_path = '../data/procesados/cdmx_enlaces_venta_deptos.json'
salida = '../data/procesados/cdmx_registros_venta_deptos.json'

with open(enlaces_path) as json_file:
    enlaces = json.load(json_file)

print(len(enlaces))

datos = []
for i,enlace in enumerate(set(enlaces)):
    if i % 50 == 0:
        print(i)
        time.sleep(30)
    code = enlace.split("-")[1]
    petlink = 'https://api.mercadolibre.com/items/MLM' + code +'?callback=jsonp1&_MELI_SDK_RANDOM=0.05949397571584673'
    data = requests.get(petlink)
    ini = data.text.find('[')
    fin = data.text.find(']',-3) + 1
    datos.append(json.loads(data.text[ini:fin])[2])

print(len(datos))

with open(salida, 'w') as fp:
    json.dump(datos, fp)