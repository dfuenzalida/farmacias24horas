#!/usr/bin/env python

import urllib2
import json
from BeautifulSoup import BeautifulSoup
from datetime import datetime

URL_GEOCODE = "http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address="

# Farmacias Region Metropolitana
URL_FARMACIAS = "http://desarrollo.redsalud.gob.cl/farmacias_turno/consultas/get_farmacias.php?region=rm+-+metropolitana"

def coordenadas_direccion(direccion):

  lat, lng = (0.0, 0.0)

  try:
    direccion = direccion.encode('utf-8')
    url = URL_GEOCODE + urllib2.quote(direccion) + ",%20CHILE"
    u = urllib2.urlopen(url)
    jsonres = json.load(u)
    loc = jsonres.get('results')[0].get('geometry').get('location')
    u.close()
    lat, lng = (loc.get("lat"), loc.get("lng"))

  except:
    pass

  return (lat, lng)

def farmacias():

  hoy = str(datetime.now().day)
  # comuna = "+".join(comuna.split(" ")) # convertir espacios en '+'
  # url = URL_COMUNA + comuna
  url = URL_FARMACIAS

  opener = urllib2.build_opener()
  opener.addheaders = [('User-agent', 'Mozilla/5.0')] # REQUERIDO!

  page = opener.open(url)
  soup = BeautifulSoup(page)
  filas = soup.findAll('tr')

  resultado = []

  for fila in filas[1:]:
    celdas = fila.findAll('td')
    dia = celdas[0].text
    if (dia == hoy):
      nombre = celdas[2].text
      direccion = celdas[3].text
      lat, lng = coordenadas_direccion(direccion)
      # print ("%s\t\t%s" % (nombre, direccion))
      resultado.append( {"nombre": nombre, "direccion": direccion, "lat": lat, "lng": lng} )

  return resultado

de_turno = farmacias()
# print (de_turno[0:3])

# carga farmacias en ambiente GAE local:
for f in de_turno:
  url = "http://192.168.0.100:8080/add?" + \
        "nombre=" + urllib2.quote(f.get("nombre").encode('utf-8')) + \
        "&direccion=" + urllib2.quote(f.get("direccion").encode('utf-8')) + \
        "&direccion_normalizada=" + urllib2.quote(f.get("direccion").encode('utf-8')) + \
        "&lat=" + urllib2.quote(str(f.get("lat"))) + \
        "&lng=" + urllib2.quote(str(f.get("lng")))
  print(url)
  opener = urllib2.build_opener()
  try:
    page = opener.open(url)
  except:
    print("ERROR al cargar %s\n" % url)

