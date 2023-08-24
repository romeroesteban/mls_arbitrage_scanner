
'''__ __ __ __           _ _  _            __ __ __          _  _     
 /_ _      __ /|     ." __      " .       /  _--_  \    . "         " . 
|_ _/    / |__|/   /  -   _ _      \     /      ___/   /      _ _      \ 
   /    / /       |    (  _ _  )    |   /   /\  \ _|  |    (  _ _  )    |        
  /_ _ / /         \               /   /__ |  \__\     \               / 
  |_ _ |/             "  _ _ _  "      |__|/  |__|        "  _ _ _  "  '''

# -*- coding: utf-8 -*-

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

from diccionarios import normalizacion
from diccionarios import ligas
from diccionarios import nombres


from scraperPlaydoit import scraperPlaydoit
from scraperCodere import scraperCodere
from buscador import buscador

# ------- E-MAIL SENDER ---------

import smtplib
from email.mime.text import MIMEText

from sendEmail import send_email

# Configuración del servidor de correo
SMTP_SERVER = 'smtp.office365.com'  # Servidor SMTP de proveedor de correo
SMTP_PORT = 587  # Puerto del servidor SMTP
SMTP_USERNAME = 'esteban98@live.com.mx'  # Tu dirección de correo electrónico
SMTP_PASSWORD = '2486753159852456'  # Tu contraseña de correo electrónico

# Verificación de la condición
def check_condition():
    # Lógica para verificar la condición
    # Devuelve True si la condición se cumple, False en caso contrario
    # Por ejemplo, supongamos que queremos verificar si un número es mayor que 10
    if busca(playdoit,codere) != []:
        return True
    else:
        return False

# ---------------------

contador = []
integridad = ""

for i in range(len(ligas['playdoit'])):
    
    print(i+1)
    
    urlpd = ligas['playdoit'][i]
    urlc = ligas['codere'][i]
    
    scraperPD = scraperPlaydoit(urlpd)
    scraperC = scraperCodere(urlc)

    scraperPD.scrapes()
    scraperC.scrapes()

    # Data Frames

    playdoitDF = scraperPD.df
    codereDF = scraperC.df

    # Formato Data Frames

    playdoitDF['Liga'] = nombres[i]
    codereDF['Liga'] = nombres[i]

    # Almacenamiento

    historico_playdoit = pd.read_csv("historico_playdoit.csv", index_col = 0)
    nuevo_playdoit = pd.concat([historico_playdoit,playdoitDF])
    nuevo_playdoit.index = range(nuevo_playdoit.shape[0])

    nuevo_playdoit.to_csv("historico_playdoit.csv")

    # Almacenamiento Codere

    historico_codere = pd.read_csv("historico_codere.csv", index_col = 0)
    nuevo_codere = pd.concat([historico_codere,codereDF])
    nuevo_codere.index = range(nuevo_codere.shape[0])

    nuevo_codere.to_csv("historico_codere.csv")

    # Integridad

    columnas_deseadas = ['Goles', 'Partido']

    if (set(columnas_deseadas).issubset(playdoitDF.columns) & set(columnas_deseadas).issubset(codereDF.columns)):
        merged = playdoitDF.merge(codereDF, left_on=["Goles", "Partido"], right_on=["Goles", "Partido"])
        integridad = integridad + ('Liga: ' + str(i) + '\nPlaydoit: '+ str(len(playdoitDF['Partido'].unique())) + '\n' + 'Codere: '+ str(len(codereDF['Partido'].unique())) + '\n' + 'Merged: ' + str(len(merged['Partido'].unique())) + '\n\n')

    # Buscador

    if (len(playdoitDF) != 0) & (len(codereDF) != 0):
        buscadorOportunidades = buscador(playdoitDF, codereDF)
        oportunidades = buscadorOportunidades.busca()
        

        if len(oportunidades) == 0:
          print('No se encontraron oportunidades de arbitraje.')

        else: 
          for oportunidad in oportunidades:
            print(oportunidad)
            contador.append(oportunidad)
            send_email("Oportunidad de Arbitraje", oportunidad)
            
    elif len(playdoitDF) == 0:
        print('No se pudieron escanear los datos de Playdoit.')
        
    elif len(codereDF) == 0:
        print('No se pudieron escanear los datos de Codere.')


if len(contador) != 0:
    body = ""
    for elemento in contador:
        body = body + elemento + '\n\n'
    send_email("Oportunidades de Arbitraje", body)
    
else: 
    send_email("No se encontraron oportunidades de arbitraje", 'Verificación de funcionamiento de script. \n\n' + integridad)    
   