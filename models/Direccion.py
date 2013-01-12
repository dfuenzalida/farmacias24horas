from google.appengine.ext import db

class Direccion(db.Model):
    nombre = db.StringProperty()
    direccion = db.StringProperty()
    direccion_normalizada = db.StringProperty()
    lat = db.FloatProperty()
    lng = db.FloatProperty()

    def __str__(self):
        return ("'%s' en '%s'" % (self.nombre, self.direccion))
