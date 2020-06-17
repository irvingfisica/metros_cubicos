import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import json
import time

def segador(url):
    enlaces = []
    active_url = url
    flag = -1
    while (flag != 0):
        time.sleep(5)
        next_page = None
        r2 = requests.get(active_url)
        print(active_url, r2.status_code)
        soup = BeautifulSoup(r2.text,features="html.parser")
        for link in soup.find_all('a'):
            enlace = link.get('href')
            clases = link.get('class')
            if clases and 'prefetch' in clases:
                next_page = enlace
            if enlace.find('/MLM') != -1:
                enlaces.append(enlace)
        if next_page:
            active_url = next_page
            flag = 1
        else:
            flag = 0
    return list(set(enlaces))

def checador(url):
    r = requests.get(url)
    status = r.status_code
    if status == 200:
        soup = BeautifulSoup(r.text,features="html.parser")
        resultado = int(soup.find(attrs={'class':'quantity-results'}).string.strip().split(" ")[0].replace(",",""))
        return resultado
    return 0

def medidor(base,ini,fin,limite,incremento):
    mult = 0
    fin_temp = ini
    resultados = 0
    while (resultados < limite) or (fin_temp > fin):
        fin_temp = ini + incremento*mult
        resultados_temp = resultados
        if (mult % 50 == 0):
            print(fin_temp,mult,resultados_temp,incremento)
        mult = mult + 1
        test = str(ini) + '-' + str(ini + incremento*mult)
        url = base + test
        resultados = checador(url)
    return (fin_temp,resultados_temp)


salida = '../data/procesados/cdmx_enlaces_venta_deptos.json'
urbase = 'https://inmuebles.metroscubicos.com/departamentos/venta/distrito-federal/'
total_final = checador(urbase)
print("total final: " + str(total_final))
base = urbase + '_PriceRange_'
ini = 0
fin = 1000000000
limite = 2000
total = 0
incremento_fix = 100000000
incremento = incremento_fix

enlaces = []
while (total + limite) < total_final:
    (fin_temp,resultados_temp) = medidor(base,ini,fin,limite,incremento)
    if resultados_temp != 0:
        print(ini,fin_temp,resultados_temp,total)
        url = base + str(ini) + '-' + str(fin_temp)
        enlaces_temp = segador(url)
        enlaces = enlaces + enlaces_temp
        ini = fin_temp
        total = total + resultados_temp
        if incremento != incremento_fix:
            incremento = incremento_fix
    else:
        incremento = int(np.floor(incremento * 0.5))
url = base + str(ini) + '-' + str(fin)
enlaces_temp = segador(url)
enlaces = enlaces + enlaces_temp

with open(salida, 'w') as fp:
    json.dump(enlaces, fp)