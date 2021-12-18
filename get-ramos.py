#!/usr/bin/python3
#coding: utf-8

import requests, re, sys
from bs4 import BeautifulSoup
from time import sleep


if len(sys.argv) != 2:
    print("\n [*] Uso de la aplicación: \n python3 get-ramos.py <rut sin digito verificador>")
    print("\n [*] Ejemplo: python3 get-ramos.py 23902132")
    sys.exit(1)


url_1 = "https://www2.duoc.cl/avance_curricular/plan?rut="

url_ramos = "https://www2.duoc.cl/avance_curricular/malla?codplan={codigoplan}&rut={rut}"

url_carreras="https://www.duoc.cl/admision/"


def carreras_duoc():
    page = requests.get(url_carreras, verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')

def get_Carrera(rut):

    page = requests.get(url_1 + rut , verify=False)

    soup = BeautifulSoup(page.content, 'html.parser')

    carrera = soup.find('div', class_="carrera")

    carrera = str(carrera)

    carrera = carrera.split()

    carrera = carrera[1:4]

    carrera = ' '.join(map(str, carrera))

    carrera = re.findall("[A-Z]\w*", carrera)

    return carrera

if __name__=='__main__':

    rut = sys.argv[1]

    carrera = get_Carrera(rut)
    if carrera == []:
        print("\n [·] Almuno no regular en Duoc UC [·] \n")
    else:
        print("\n {} \n ".format(carrera))
    # page = requests.get(url , verify=False)

    # soup = BeautifulSoup(page.content, 'html.parser')

    # print(soup)

