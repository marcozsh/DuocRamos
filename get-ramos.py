#!/usr/bin/python3
#coding: utf-8

import requests, re, sys
from bs4 import BeautifulSoup
from time import sleep


if len(sys.argv) != 2:
    print("\n [!] Uso de la aplicación: \n python3 get-ramos.py <rut sin dígito verificador> [!] \n")
    print("\n [·] Ejemplo: python3 get-ramos.py 23902132 [·] \n")
    sys.exit(1)


url_1 = "https://www2.duoc.cl/avance_curricular/plan?rut="


def get_pag(rut):
    #page = requets.get(url_1 + rut, verify=False) <- descomentar esta línea si da error del certificado

    request_page = requests.get(url_1 + rut) # <- comentar esta línea si descomentas la línea de arriba

    page = BeautifulSoup(request_page.content, 'html.parser')

    return page, request_page.cookies

def get_carrera(page):

    carrera = page.find('div', class_="carrera")

    carrera = str(carrera)

    carrera = carrera.split()

    carrera = carrera[1:4]

    carrera = ' '.join(map(str, carrera))

    carrera = re.findall("[A-Z]\w*", carrera)

    return carrera

def get_malla(pag, rut):

    cod = pag.find('div', class_="cod")
    cod = re.findall("\d{1,100}", str(cod))[0]

    page_malla = requests.get("https://www2.duoc.cl/avance_curricular/malla?codplan={}&rut={}".format(cod, rut)
                        ,cookies=get_pag(rut)[1])

    page = BeautifulSoup(page_malla.content, 'html.parser')

    return page

def get_student_data(pag):

    #Student Name

    student_name = pag.find('div', class_="name")
    student_name = re.findall("[A-Z]\w*", str(student_name))
    student_name.remove("Nombre")
    student_name = ' '.join(map(str, student_name))

    #End Student Name

    #Student rut

    student_rut = pag.find('div', class_="rut")
    student_rut = re.findall("[0-9~@#\^\$&\*\(\)-\.\?\d]*", str(student_rut))
    student_rut = ' '.join(map(str, student_rut))
    student_rut = student_rut.replace(' ', '')

    #End Student rut

    # Student Malla

    student_malla = pag.find('div', class_="malla-general")
    student_malla = pag.find('div', class_="malla-general")
    student_malla = pag.findAll('script')

    #End Student Malla
    return student_name, student_rut, student_malla

if __name__=='__main__':

    rut = sys.argv[1]

    page = get_pag(rut)[0]

    carrera = get_carrera(page)

    # print(get_malla(page, rut))

    print(get_student_data(get_malla(page,rut))[2])

    # if carrera == []:
        # print("\n [!] Almuno no regular en Duoc UC [!] \n")
    # else:
        # carrera = ' '.join(map(str, carrera))

        # print("\n [*] {} [*] \n".format(get_student_data(get_malla(page, rut))[0])) # Name

        # print("\n [*] {} [*] \n".format(get_student_data(get_malla(page, rut))[1])) # Rut

        # print("\n  [*] {} [*] \n ".format(carrera)) # Carrera

        # print("\n {} \n".format(get_malla(page, rut)))



