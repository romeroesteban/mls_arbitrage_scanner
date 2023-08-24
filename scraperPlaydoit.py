import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

import os
import datetime

import pandas as pd
import numpy as np

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException 
from selenium.common.exceptions import InvalidSessionIdException

from diccionarios import normalizacion
from diccionarios import ligas

class scraperPlaydoit():

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
    fecha_actual = datetime.datetime.now()
    dia_actual = str(fecha_actual).split(" ",1)[0]
    hora_actual = str(fecha_actual).split(" ",1)[1]
    hora_actual = str(hora_actual.split(":",2)[0]) + ':' + str(hora_actual.split(":",2)[1])

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
        return

    # Navegar a la página
    driver.get(self.url)

    # Crear una instancia de ActionChains
    actions = ActionChains(driver)

    wait = WebDriverWait(driver, 10)
    
    try: 
        elementos_clicables = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="_asb_events-tree-table "]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]')))
    except TimeoutException:      
        try:
            elementos_clicables = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="_asb_events-tree-table "]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]')))
        except TimeoutException:
            print('Formato de página no compatible.')
            return
        
    dias_lista = []
    meses_lista = []
    horas_lista = []

    # Fecha y hora
    try:
        fechaYHora = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_asb_events-tree-table "]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/div/div/div[@class="asb-text"]')))
        for elemento in fechaYHora:
            dias_lista.append(elemento.text.split(" • ",1)[0].split("/",1)[0])
            meses_lista.append(elemento.text.split(" • ",1)[0].split("/",1)[1])
            horas_lista.append(elemento.text.split(" • ",1)[1])
    except TimeoutException:
        print('Problemas al recolectar fechas')
        return
    except StaleElementReferenceException:
        return

    lista_urls = []
    lista_partidos = []
    control = len(elementos_clicables)
    for i in range(len(elementos_clicables)):

        try:
          driver.get(self.url)
        except WebDriverException:
          print('Algo salió mal al intentar cargar el url')
          continue

        wait = WebDriverWait(driver, 10)

        # Locate the clickable elements again after navigating to a new URL
        try: 
            elementos_clicables = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="_asb_events-tree-table "]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]')))
        except TimeoutException:      
            try:
                elementos_clicables = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="_asb_events-tree-table "]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]')))
            except TimeoutException:
                print('Formato de página no compatible.')
                continue
            except WebDriverException:
                print('WebDriverException')
                continue
        except WebDriverException:      
            try:
                elementos_clicables = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="_asb_events-tree-table "]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]')))
            except TimeoutException:
                print('Formato de página no compatible.')
                continue
            except WebDriverException:
                print('WebDriverException')
                continue

        try:
            oponentes = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="_asb_events-tree-table "]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]')))
        except TimeoutException:      
            try:
                oponentes = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="_asb_events-tree-table "]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]')))
            except TimeoutException:
                print('Formato de página no compatible.')
                continue
            except WebDriverException:
                print('WebDriverException')
                continue
        except WebDriverException:      
            try:
                oponentes = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="_asb_events-tree-table "]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]')))
            except TimeoutException:
                print('Formato de página no compatible.')
                continue
            except WebDriverException:
                print('WebDriverException')
                continue

        teams = []

        if i < len(elementos_clicables):
            teams.append(self.normaliza(elementos_clicables[i].text))
        else:
            continue
        if i < len(oponentes):
            teams.append(self.normaliza(oponentes[i].text))
        else:
            continue

        sort = sorted(teams)

        # Ejecutar el script para hacer clic en el elemento
        driver.execute_script("arguments[0].click();", elementos_clicables[i])

        # Esperar un breve tiempo para que se realice el clic
        time.sleep(2)

        # Obtener el URL después de hacer clic en el elemento
        try:
            url = driver.current_url
            lista_urls.append(url)
        except WebDriverException as e:
            print("Error al obtener la URL actual:", e)
            continue 


        lista_partidos.append(sort[0] + ' vs ' + sort[1])

    dfplaydoit = []
    i = 0
    for url in lista_urls:
        try:
          driver.get(url)
        except WebDriverException:
          print('Algo salió mal al intentar cargar el url')
          continue
        except InvalidSessionIdException:
            print('InvalidSessionIdException')
            continue

        # Listas
        goles_lista = []
        mas_lista = []
        menos_lista = []

        menos_bu = []
        mas_bu = []

        # Goles
        try:
            goles = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_asb_event-details-markets-group "]/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[2]/div[1]/div'))
            )
        except TimeoutException:
            continue

        # Mas
        try:
            mas = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_asb_event-details-markets-group "]/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[2]/div[2]/span'))
            )
        except TimeoutException:
            mas = []
            for elemento in goles:
                mas_bu.append(-1111)

        # Menos
        try:
            menos = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_asb_event-details-markets-group "]/div[3]/div[2]/div/div/div[2]/div/div/div/div/div[2]/div[2]/span'))
            )
        except TimeoutException:
            menos = []
            for elemento in goles:
                menos_bu.append(-1111)
    

        for elemento in goles:
            try:
                goles_lista.append(elemento.text.replace("Más de ", ""))
            except StaleElementReferenceException:
                continue

        for elemento in mas:
            try:
                mas_lista.append(elemento.text.replace("+",""))
            except StaleElementReferenceException:
                continue

        for elemento in menos:
            try:
                menos_lista.append(elemento.text.replace("+",""))
            except StaleElementReferenceException:
                continue


        if ((len(goles_lista) == len(mas_lista)) & (len(goles_lista) == len(menos_lista))):
            dic = {'Goles': goles_lista, 'Más de ': mas_lista, 'Menos de ': menos_lista}
            df = pd.DataFrame(dic)
            df['Partido'] = lista_partidos[i]
            df['Hora de Recolección'] = hora_actual
            df['Día de Recolección'] = dia_actual

            if (len(lista_partidos)==len(horas_lista)):
                df['Mes'] = meses_lista[i]
                df['Día'] = dias_lista[i]
                df['Hora'] = horas_lista[i]
            else:
                df['Mes'] = 'NaN'
                df['Día'] = 'NaN'
                df['Hora'] = 'NaN'
                print(str(len(lista_partidos)) + ' ' + str(len(horas_lista)))

            dfplaydoit.append(df)

        elif ((len(goles_lista) == len(mas_bu)) & (len(goles_lista) == len(menos_bu))):
            dic = {'Goles': goles_lista, 'Más de ': mas_bu, 'Menos de ': menos_bu}
            df = pd.DataFrame(dic)
            df['Partido'] = lista_partidos[i]
            df['Hora de Recolección'] = hora_actual
            df['Día de Recolección'] = dia_actual

            if (len(lista_partidos)==len(horas_lista)):
                df['Mes'] = meses_lista[i]
                df['Día'] = dias_lista[i]
                df['Hora'] = horas_lista[i]
            else:
                df['Mes'] = 'NaN'
                df['Día'] = 'NaN'
                df['Hora'] = 'NaN'
                print(str(len(lista_partidos)) + ' ' + str(len(horas_lista)))

            dfplaydoit.append(df)

        i += 1

    playdoit = pd.DataFrame()
    for df in dfplaydoit:
        playdoit = pd.concat([playdoit,df])
    playdoit.index = range(playdoit.shape[0])

    self.df = playdoit
