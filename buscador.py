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

class buscador():

  def __init__(self, casaUno, casaDos):
    self.casaUno = casaUno
    self.casaDos = casaDos

  def convierteMomio(self,americano):
    if americano < 100:
        return (100/(-americano))+1
    else:
        return (americano+100)/100

  def encuentra(self,a,b):
      p1 = 1/(self.convierteMomio(a))
      p2 = 1/(self.convierteMomio(b))
      
      if (p1+p2) < 1:

          # Ganancias
          r1 = self.convierteMomio(a)*(self.calculaMontos(p1,p2)[0]) - self.calculaMontos(p1,p2)[0] - self.calculaMontos(p1,p2)[1]
          r2 = self.convierteMomio(b)*(self.calculaMontos(p1,p2)[1]) - self.calculaMontos(p1,p2)[1] - self.calculaMontos(p1,p2)[0]
          
          r1 = round(r1,4)
          r2 = round(r2,4)

          return "Oportunidad de arbitraje.\n" \
                "-------------------------\n" \
                "Casa 1: " + str(self.calculaMontos(p1, p2)[0]) + '(' + str(a) + ')' + "\n" \
                "Casa 2: " + str(self.calculaMontos(p1, p2)[1]) + '(' + str(b) + ')' + "\n" \
                "Rendimiento entre: " + str(r1 * 100) + "%" + " y " + str(r2 * 100) + "%"
          
      else:
          return 'No hay oportunidad de arbitraje.'
          
  def calculaMontos(self, p1,p2):
      margen = 1 - (p1 + p2)
      factor = 1/margen
      
      # Porcentajes de asignación
      a1 = p1 * factor
      a2 = p2 * factor
      
      m1 = (a1/(a1 + a2))
      m2 = (a2/(a1 + a2))
      
      return round(m1,4), round(m2,4)

  def busca(self):
      merged = self.casaUno.merge(self.casaDos, left_on=["Goles", "Partido"], right_on=["Goles", "Partido"])
      oportunidades = []

      for i in range(len(merged)):
          mas_playdoit = int(merged.loc[i,'Más de _x'])
          menos_codere = int(merged.loc[i,'Menos de _y'])

          if self.encuentra(mas_playdoit, menos_codere) != 'No hay oportunidad de arbitraje.':
              oportunidades.append("Más de " + merged.loc[i,"Goles"] +" en Playdoit, menos en Codere\n" + merged.loc[i,'Partido'] + '\n' + self.encuentra(mas_playdoit,menos_codere))
          else:
              continue

      for i in range(len(merged)):
          mas_codere = int(merged.loc[i,'Más de _y'])
          menos_playdoit = int(merged.loc[i,'Menos de _x'])

          if self.encuentra(mas_codere, menos_playdoit) != 'No hay oportunidad de arbitraje.':
              oportunidades.append("Más de " + merged.loc[i,"Goles"] +" en Codere, menos en Playdoit\n" + merged.loc[i,'Partido'] + '\n' + self.encuentra(mas_codere, menos_playdoit))
          else:
              continue        

      return oportunidades