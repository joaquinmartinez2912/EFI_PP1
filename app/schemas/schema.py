from app import ma
from marshmallow import fields

# Serializar es de Py a JSON (dump)

class UsuarioSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()
    correo = fields.String()
    contrasena = fields.String()

class CategoriasSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String

class EntradaSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    titulo = fields.String
    contenido = fields.String
    fecha = fields.String
    autor_obj = fields.Nested(UsuarioSchema, exclude=("id","correo","contrasena"))
    etiqueta_obj = fields.Nested(CategoriasSchema, exclude=("id",))

class ComentariosSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    contenido = fields.String
    fecha = fields.String
    autor_obj = fields.Nested(UsuarioSchema, exclude=("id","correo","contrasena"))
    eti_obj = fields.Nested(EntradaSchema, exclude=("id","contenido","fecha","autor_obj","etiqueta_obj"))
