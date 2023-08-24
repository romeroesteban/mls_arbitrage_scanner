import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

import os

import pandas as pd
import numpy as np

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException 

from diccionarios import normalizacion
from diccionarios import ligas

import traceback

class scraperCodere():

  def __init__(self, url):
    self.url = url
    self.df = pd.DataFrame()

  def normaliza(self, string):
      diccionario = normalizacion
      if string in diccionario:
          return diccionario[string]
      else:
          return string

  def scrapes(self):
    # Configurar el servicio de ChromeDriver
    service = Service(ChromeDriverManager().install())

    # Configurar las opciones del navegador
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Para ejecutar Chrome en modo headless (sin interfaz gráfica)

    # Inicializar el navegador
    try: 
        driver = webdriver.Chrome(options=options)
    except WebDriverException:
        print('Problemas al inicializar el navegador.')
        print(str(WebDriverException))  # Imprimir el mensaje de error de la excepción
        print(traceback.format_exc())
        return
  
    driver.get(self.url)


    # Partidos
    try: 
      tablas_partidos = WebDriverWait(driver, 3).until(
              EC.presence_of_all_elements_located((By.XPATH, '//*[@id="main-area"]/div[2]/div/div'))
          )
    except TimeoutException:
                print('No hay partidos.') 
                return

    partidos = []
    for i in range(2, len(tablas_partidos) + 1):

        xpath = '//*[@id="main-area"]/div[2]/div/div[' + str(i) + ']/h6/span'
        try:
            partido = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except TimeoutException:
                continue

        sep = ' v '   
        teams = []

        teams.append(self.normaliza(partido.text.split(sep,1)[0]))
        teams.append(self.normaliza(partido.text.split(sep,1)[1]))

        sort = sorted(teams)

        partidos.append(sort[0] + ' vs ' + sort[1])

    dfcodere = []

    for i in range(2, len(partidos) + 2):
        menos_bu = []
        mas_bu = []

        # Goles
        j = str(i)
        xpath_goles = '//*[@id="main-area"]/div[2]/div/div[' + j + ']/div/table/tbody/tr/td[1]/div/button/span/span/span/span[2]'
        try:
            goles = WebDriverWait(driver, 3).until(
                    EC.presence_of_all_elements_located((By.XPATH, xpath_goles))
                )
        except TimeoutException:
                continue

        # Mas
        xpath_mas = '//*[@id="main-area"]/div[2]/div/div[' + j + ']/div/table/tbody/tr/td[1]/div/button/span/span[4]'
        try:
             mas = WebDriverWait(driver, 3).until(
                    EC.presence_of_all_elements_located((By.XPATH, xpath_mas))
                )
        except TimeoutException:
                mas = []
                for elemento in goles:
                    mas_bu.append(-1111)

        # Menos
        xpath_menos = '//*[@id="main-area"]/div[2]/div/div[' + j + ']/div/table/tbody/tr/td[2]/div/button/span/span[4]'
        try:
             menos = WebDriverWait(driver, 3).until(
                    EC.presence_of_all_elements_located((By.XPATH, xpath_menos))
                )
        except TimeoutException:
                menos = []
                for elemento in goles:
                    menos_bu.append(-1111)

        # Listas
        goles_lista = []
        mas_lista = []
        menos_lista = []

        for elemento in goles:
            goles_lista.append(elemento.text)

        for elemento in mas:
            mas_lista.append(elemento.text.replace("+",""))

        for elemento in menos:
            menos_lista.append(elemento.text.replace("+",""))

        if ((len(goles_lista) == len(mas_lista)) & (len(goles_lista) == len(menos_lista))):
            dic = {'Goles': goles_lista, 'Más de ': mas_lista, 'Menos de ': menos_lista}
            df = pd.DataFrame(dic)
            df['Partido'] = partidos[i-2]

            dfcodere.append(df)
        
        elif ((len(goles_lista) == len(mas_bu)) & (len(goles_lista) == len(menos_bu))):
            dic = {'Goles': goles_lista, 'Más de ': mas_bu, 'Menos de ': menos_bu}
            df = pd.DataFrame(dic)
            df['Partido'] = partidos[i-2]

            dfcodere.append(df)

    codere = pd.DataFrame()
    for df in dfcodere:
        codere = pd.concat([codere,df])
    codere.index = range(codere.shape[0])

    self.df = codere