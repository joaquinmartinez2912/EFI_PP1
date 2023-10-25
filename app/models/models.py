from app import db
from sqlalchemy import ForeignKey

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer,primary_key = True)
    nombre = db.Column(db.String(50),nullable = False)
    correo = db.Column(db.String(50),nullable = False)
    contrasena = db.Column(db.String(50),nullable = False)

    def __str__(self):
        return self.nombre

class Categorias(db.Model):
    __tablename__ = "categoria"
    id = db.Column(db.Integer,primary_key = True)
    nombre = db.Column(db.String(50),nullable = False)

    def __str__(self):
        return self.nombre

class Entrada(db.Model):
    __tablename__ = "entrada"
    id = db.Column(db.Integer,primary_key = True)
    titulo = db.Column(db.String(50),nullable = False)
    contenido = db.Column(db.String(140),nullable = False)
    fecha = db.Column(db.String(50),nullable = False)
    autor = db.Column(
                    db.Integer,
                    ForeignKey("usuarios.id"),
                    nullable=False )
    etiqueta = db.Column(
                    db.Integer,
                    ForeignKey("categoria.id"),
                    nullable=False )
    
    autor_obj = db.relationship("Usuario")
    etiqueta_obj = db.relationship("Categorias")

    def __str__(self):
        return self.titulo

class Comentarios(db.Model):
    __tablename__ = "comentario"
    id = db.Column(db.Integer,primary_key = True)
    contenido = db.Column(db.String(140),nullable = False)
    fecha = db.Column(db.String(50),nullable = False)
    autor = db.Column(
                    db.Integer,
                    ForeignKey("usuarios.id"),
                    nullable=False )
    etiqueta = db.Column(
                    db.Integer,
                    ForeignKey("entrada.id"),
                    nullable=False )

    autor_obj = db.relationship("Usuario")
    eti_obj = db.relationship("Entrada")

    def __str__(self):
        return self.titulo

