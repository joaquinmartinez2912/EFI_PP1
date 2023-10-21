from flask import (Flask,
    render_template,
    redirect,
    request,    
    url_for)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

app = Flask(__name__)

#mysql+pymysql://usuario:contraseña@ip/nombre_db
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://BD2021:BD2021itec@143.198.156.171/db_joaquinppp"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Clases:

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

    def __str__(self):
        return self.titulo


# Rutas

@app.context_processor
def inject_paises():
    cat = db.session.query(Categorias).all()
    ent = db.session.query(Entrada).all()
    usu = db.session.query(Usuario).all()
    coments = db.session.query(Comentarios).all()
    return dict(
        listaCategorias=cat,
        listaEntradas=ent,
        listaUsuarios=usu,
        listaComentarios=coments
    )


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/principal",methods=["GET", "POST"])
def main():
    if request.method == "POST":
        nombreCargado = request.form["usuarioActivo"]
        # uso la funcion filter_by porque con get solo puedo buscar por PK que es el id.
        usActivo = db.session.query(Usuario).filter_by(nombre=nombreCargado).first()

        # Lo paso como parametro en el render_template
        return render_template("main.html", UsAct = usActivo)


@app.route("/comentarios",methods=["POST"])
def comentarios():
    if request.method == "POST":
        entradaId = request.form["identrada"]
        usActivoid = request.form["usuarioActivo"]
       
        usActivo = db.session.query(Usuario).filter_by(id=usActivoid).first()

        entradas = db.session.query(Entrada).all()
        objetoEntrada = ""
        for entrada in entradas:
            if int(entrada.id) == int(entradaId):
                objetoEntrada = entrada

        return render_template("comentarios.html", enActiva = objetoEntrada, UsAct = usActivo )
       

@app.route("/usuarios")
def user():
    return render_template("users.html")


@app.route("/agregarUsuario",methods=["POST"])
def agregarUsuario():
    if request.method == "POST":
        nombreUsuario = request.form["usuario"]
        correoUsuario = request.form["correo"]
        contrasenaUsuario = request.form["contra"]

        nuevoUsuario = Usuario(nombre=nombreUsuario, correo=correoUsuario, contrasena=contrasenaUsuario)
        db.session.add(nuevoUsuario)
        db.session.commit()

        return redirect(url_for("index"))


@app.route("/agregarPosteo", methods=["GET", "POST"])
def agregarPost():
    if request.method == "POST":
        fechaPost = request.form["fecha"]
        tituloPost = request.form["titulo"]
        textoPost = request.form["texto"]
        etiquetaPost = request.form["categ"]
        usuarioId = request.form["idUsuario"]

        # Usuario para cuando recargue la pagina.
        usActivo = db.session.query(Usuario).filter_by(id=usuarioId).first()
        
        #Id para carga de base de datos.
        cat = db.session.query(Categorias).all()
        etiquetaId = ""
        for cate in cat:
            if cate.nombre == etiquetaPost:
                etiquetaId = cate.id
        
        nuevoPost = Entrada(titulo=tituloPost, contenido=textoPost, fecha=fechaPost, autor=usuarioId, etiqueta=etiquetaId )
        db.session.add(nuevoPost)
        db.session.commit()
        
        return render_template("main.html", UsAct = usActivo)


@app.route("/agregarComentario", methods=["GET", "POST"])
def agregarComentario():
    if request.method == "POST":
        fechaComent = request.form["fecha"]
        textoComent = request.form["texto"]
        usuarioId = request.form["idUsuario"]
        entradaId = request.form["idEntrada"]

        # entrada para cuando recargue la pagina.
        objetoEntrada = db.session.query(Entrada).filter_by(id=entradaId).first()

        #Id para carga de base de datos.
        usuBase = db.session.query(Usuario).all()
        usuNombre = ""
        for usuario in usuBase:
            if usuario.id == int(usuarioId):
                usActivo = usuario
        
        nuevoComent = Comentarios(contenido=textoComent, fecha=fechaComent, autor=usuarioId, etiqueta=entradaId )
        db.session.add(nuevoComent)
        db.session.commit()
        
        return render_template("comentarios.html",enActiva = objetoEntrada, UsAct = usActivo)
        
