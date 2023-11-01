from app import ma
from marshmallow import fields

# Serializar es de Py a JSON (dump)

class UsuarioPostSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()
    correo = fields.String()
    contrasena = fields.String()

    def saludo(self, obj):
        return f"Datos de usuario {obj.nombre}"
    
class UsuarioGetSchema(UsuarioPostSchema):
    class Meta:
        exclude = ("id","contrasena")

    saludo = fields.Method("saludo")

class CategoriaGetSchema(ma.Schema):
    nombre = fields.String()

class CategoriaPostSchema(CategoriaGetSchema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()
    
class EntradaGetSchema(ma.Schema):
    titulo = fields.String()
    contenido = fields.String()
    fecha = fields.String()
    autor_obj = fields.Nested(UsuarioGetSchema, exclude=("correo","saludo"))
    etiqueta_obj = fields.Nested(CategoriaGetSchema)

class EntradaPostSchema(EntradaGetSchema):
    id = fields.Integer(dump_only=True)
    autor = fields.Integer()
    etiqueta = fields.Integer()


class ComentariosSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    contenido = fields.String()
    fecha = fields.String()
    #autor_obj = fields.Nested(UsuarioSchema, exclude=("id","correo","contrasena"))
    #eti_obj = fields.Nested(EntradaGetSchema, exclude=("contenido","fecha","autor_obj","etiqueta_obj"))
