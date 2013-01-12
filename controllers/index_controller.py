from google.appengine.api import datastore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from controllers.base_controller import BaseController
from models.Direccion import Direccion

# import os
import simplejson as json

class IndexController(BaseController):
    def get(self):
        # alumnos = datastore.Query("Alumno", _namespace=None).Get(100)
        self.render('index', {'nums': [] })

class AgregaDireccionController(BaseController):
    def get(self):
        direccion = Direccion()
        direccion.nombre = self.request.get("nombre").encode("utf-8")
        direccion.direccion = self.request.get("direccion")
        direccion.direccion_normalizada = self.request.get("direccion_normalizada")
        direccion.lat = float(self.request.get("lat"))
        direccion.lng = float(self.request.get("lng"))
        direccion.put()
        self.redirect("/list")

class ListaDireccionesController(BaseController):
    def get(self):
        direcciones = datastore.Query("Direccion", _namespace=None).Get(100)
        # self.render('lista', {'direcciones': direcciones })
        jsonlist = json.dumps(direcciones)
        self.response.out.write(jsonlist)

application = webapp.WSGIApplication(
    [('/', IndexController),
     ('/list', ListaDireccionesController),
     ('/add', AgregaDireccionController),
    ],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
