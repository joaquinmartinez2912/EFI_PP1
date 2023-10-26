from app import app, db

from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
# Imports de variables generadas por nosotros
from app.models.models import (
    Usuario,
    Entrada,
    Categorias,
    Comentarios
)

from app.schemas.schema import (
    UsuarioSchema,
    CategoriasSchema,
    EntradaSchema,
    ComentariosSchema
)

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
    return render_template(
        'index.html'
    )

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

@app.route("/add_user", methods=["POST"])
def add_user():
    user_json = request.get_json()
    user_json = UsuarioSchema().load(request.json)
    nombre = user_json.get("nombre")
    correo = user_json.get("correo") 
    contrasena = user_json.get("contrasena")
    print(nombre,correo,contrasena)

    nuevoUsuario = Usuario(nombre=nombre, correo=correo, contrasena=contrasena)
    db.session.add(nuevoUsuario)
    db.session.commit()

    return jsonify({
        "Usuario creado exitosamente ?": "Si",
        "nombre" : nombre,
        "correo": correo
    }, 200)

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
        
