from app import app, db
from werkzeug.exceptions import NotFound
from marshmallow import ValidationError

from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# Imports de variables generadas por nosotros
from app.models.models import Usuario, Entrada, Categorias, Comentarios

from app.schemas.schema import (
    UsuarioGetSchema,
    UsuarioPostSchema,
    CategoriaGetSchema,
    CategoriaPostSchema,
    EntradaGetSchema,
    EntradaPostSchema,
    ComentariosGetSchema,
    ComentariosPostSchema
)

from flask.views import MethodView

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error="La ruta ingresada no se encuentra definida"), 404

class UserAPI(MethodView):
    def get(self, user_id=None):
        if user_id is None:
            usuarios = Usuario.query.all()
            resultado = UsuarioGetSchema().dump(usuarios, many=True)
        else:
            usuario = Usuario.query.get(user_id)
            resultado = UsuarioGetSchema().dump(usuario)
        return jsonify(resultado)

    def post(self):
        try:
            user_json = request.get_json()
            user_json = UsuarioPostSchema().load(request.json)

            nombre = user_json.get("nombre")
            correo = user_json.get("correo")
            contrasena = user_json.get("contrasena")
            password_hash = generate_password_hash(
             contrasena, method='pbkdf2', salt_length=8
             )

            nuevoUsuario = Usuario(nombre=nombre, correo=correo, contrasena=password_hash)
            db.session.add(nuevoUsuario)
            db.session.commit()

            return jsonify(
                {
                    "Usuario creado exitosamente ?": "Si",
                    "nombre": nombre,
                    "correo": correo,
                    "contraseña": password_hash
                },
                200,
            )
        except ValidationError:
            return jsonify(
                {
                    "error": "Error de validación",
                },
                400,
            )
        except NotFound:
            return jsonify(
                {
                    "error": "Recurso no encontrado",
                },
                404,
            )
        except Exception:
            return jsonify(
                {
                    "error": "Error en el servidor",
                },
                500,
            )
        
    def put(self, user_id):
        usuario = Usuario.query.get(user_id)

        if usuario is None:
            return jsonify(Mensaje=f"No existe usuario con ID:{user_id}"), 404
        try:
            user_json = UsuarioGetSchema().load(request.json)
            nuevo_correo = user_json.get("correo")

            usuario.correo = nuevo_correo
            db.session.commit()
            return jsonify(Mensaje=f"Se modifico el correo del usuario de ID:{user_id}")
        except ValidationError:
            return jsonify(
                {
                    "error": "Error de validación",
                },
                400,
            )
        except Exception:
            return jsonify(
                {
                    "error": "Error en el servidor",
                },
                500,
            )
        
    def delete(self, user_id):
        usuario = Usuario.query.get(user_id)
        if usuario is None:
            return jsonify(Mensaje=f"No existe usuario con ID:{user_id}"), 404
        db.session.delete(usuario)
        db.session.commit()
        return jsonify(Mensaje=f"Se borro el usuario de ID {user_id}")


app.add_url_rule("/users", view_func=UserAPI.as_view("usuarios"))
app.add_url_rule("/users/<user_id>", view_func=UserAPI.as_view("usuario_por_id"))


class PostAPI(MethodView):
    def get(self, post_id=None):
        if post_id is None:
            entrada = Entrada.query.all()
            resultado = EntradaGetSchema().dump(entrada, many=True)
        else:
            entrada = Entrada.query.get(post_id)
            resultado = EntradaGetSchema().dump(entrada)
        return jsonify(resultado)

    def post(self):
        try:
            post_json = request.get_json()
            post_json = EntradaPostSchema().load(request.json)

            titulo = post_json.get("titulo")
            contenido = post_json.get("contenido")
            fecha = post_json.get("fecha")
            autor = post_json.get("autor")
            etiqueta = post_json.get("etiqueta")

            nuevoPost = Entrada(
                titulo=titulo,
                contenido=contenido,
                fecha=fecha,
                autor=autor,
                etiqueta=etiqueta,
            )
            db.session.add(nuevoPost)
            db.session.commit()

            return jsonify(
                {
                    "titulo": titulo,
                    "contenido": contenido,
                    "autor": nuevoPost.autor_obj.nombre,
                    "etiqueta": nuevoPost.etiqueta_obj.nombre,
                },
                200,
            )
        except ValidationError:
            return jsonify(
                {
                    "error": "Error de validación",
                },
                400,
            )
        except NotFound:
            return jsonify(
                {
                    "error": "Recurso no encontrado",
                },
                404,
            )
        except Exception:
            return jsonify(
                {
                    "error": "Error en el servidor",
                },
                500,
            )

    def put(self, post_id):
        post = Entrada.query.get(post_id)

        if post is None:
            return jsonify(Mensaje=f"No existe post con ID:{post_id}"), 404
        try:
            post_json = EntradaGetSchema().load(request.json)
            nuevo_titulo = post_json.get("titulo")

            post.titulo = nuevo_titulo
            db.session.commit()
            return jsonify(Mensaje=f"Se modifico el titulo del post de ID:{post_id}")
        except ValidationError:
            return jsonify(
                {
                    "error": "Error de validación",
                },
                400,
            )
        except Exception:
            return jsonify(
                {
                    "error": "Error en el servidor",
                },
                500,
            )
        
    def delete(self, post_id):
        post = Entrada.query.get(post_id)
        if post is None:
            return jsonify(Mensaje=f"No existe post con ID:{post_id}"), 404
        db.session.delete(post)
        db.session.commit()
        return jsonify(Mensaje=f"Se borro el post de ID {post_id}")

app.add_url_rule("/posts", view_func=PostAPI.as_view("entrada"))
app.add_url_rule("/posts/<post_id>", view_func=PostAPI.as_view("entrada_por_id"))


class CategoriaAPI(MethodView):
    def get(self, cate_id=None):
        if cate_id is None:
            categorias = Categorias.query.all()
            resultado = CategoriaGetSchema().dump(categorias, many=True)
        else:
            categorias = Categorias.query.get(cate_id)
            resultado = CategoriaGetSchema().dump(categorias)
        return jsonify(resultado)

    def post(self):
        try:
            cate_json = request.get_json()
            cate_json = CategoriaPostSchema().load(request.json)

            nombre = cate_json.get("nombre")

            nuevaCate = Categorias(nombre=nombre)
            db.session.add(nuevaCate)
            db.session.commit()

            return jsonify({"nombre": nombre}, 200)
        except ValidationError:
            return jsonify(
                {
                    "error": "Error de validación",
                },
                400,
            )
        except NotFound:
            return jsonify(
                {
                    "error": "Recurso no encontrado",
                },
                404,
            )
        except Exception:
            return jsonify(
                {
                    "error": "Error en el servidor",
                },
                500,
            )

    def put(self, cate_id):
        cate = Categorias.query.get(cate_id)

        if cate is None:
            return jsonify(Mensaje=f"No existe categoria con ID:{cate_id}"), 404
        try:
            cate_json = CategoriaGetSchema().load(request.json)
            nombre_nuevo = cate_json.get("nombre")

            cate.nombre = nombre_nuevo
            db.session.commit()
            return jsonify(Mensaje=f"Se modifico el titulo del categoria de ID:{cate_id}")
        except ValidationError:
            return jsonify(
                {
                    "error": "Error de validación",
                },
                400,
            )
        except Exception:
            return jsonify(
                {
                    "error": "Error en el servidor",
                },
                500,
            )
        
    def delete(self, cate_id):
        cate = Categorias.query.get(cate_id)
        if cate is None:
            return jsonify(Mensaje=f"No existe cate con ID:{cate_id}"), 404
        db.session.delete(cate)
        db.session.commit()
        return jsonify(Mensaje=f"Se borro la categoria de ID {cate_id}")

app.add_url_rule("/cats", view_func=CategoriaAPI.as_view("categorias"))
app.add_url_rule("/cats/<cate_id>", view_func=CategoriaAPI.as_view("categorias_por_id"))


class ComentariosAPI(MethodView):
    def get(self, post_id=None):
        if post_id is None:
            comentario = Comentarios.query.all()
            resultado = ComentariosGetSchema().dump(comentario, many=True)
        else:
            entrada = Entrada.query.get(post_id)
            if entrada is None:
                return jsonify({"Mensaje": "Ese id de posteo no existe"}, 404)
            
            comentarios = Comentarios.query.filter_by(etiqueta=int(post_id)).all()
            if len(comentarios) != 0:
                resultado = ComentariosGetSchema().dump(comentarios, many=True)
            else:
                return jsonify({"Mensaje": "Ese id de posteo no tiene comentarios"})
        return jsonify(resultado)

    def post(self):
        try:
            coment_json = request.get_json()
            coment_json = ComentariosPostSchema().load(request.json)

            contenido = coment_json.get("contenido")
            fecha = coment_json.get("fecha")
            autor = coment_json.get("autor")
            etiqueta = coment_json.get("etiqueta")

            nuevoComent = Comentarios(
                contenido=contenido, fecha=fecha, autor=autor, etiqueta=etiqueta
            )
            db.session.add(nuevoComent)
            db.session.commit()

            return jsonify(
                {"comentario": contenido, "autor": nuevoComent.autor_obj.nombre, "posteo": nuevoComent.eti_obj.titulo}, 200
            )
        except ValidationError:
            return jsonify(
                {
                    "error": "Error de validación",
                },
                400,
            )
        except NotFound:
            return jsonify(
                {
                    "error": "Recurso no encontrado",
                },
                404,
            )
        except Exception:
            return jsonify(
                {
                    "error": "Error en el servidor",
                },
                500,
            )

    def put(self, coment_id):
        coment = Comentarios.query.get(coment_id)

        if coment is None:
            return jsonify(Mensaje=f"No existe comentario con ID:{coment_id}"), 404
        try:
            coment_json = ComentariosGetSchema().load(request.json)
            conte_nuevo = coment_json.get("contenido")

            coment.contenido = conte_nuevo
            db.session.commit()
            return jsonify(Mensaje=f"Se modifico el contenido del comentario de ID:{coment_id}")
        except ValidationError:
            return jsonify(
                {
                    "error": "Error de validación",
                },
                400,
            )
        except Exception:
            return jsonify(
                {
                    "error": "Error en el servidor",
                },
                500,
            )
        
    def delete(self, coment_id):
        coment = Comentarios.query.get(coment_id)
        if coment is None:
            return jsonify(Mensaje=f"No existe comentario con ID:{coment_id}"), 404
        db.session.delete(coment)
        db.session.commit()
        return jsonify(Mensaje=f"Se borro el comentario de ID {coment_id}")

app.add_url_rule("/coments", view_func=ComentariosAPI.as_view("comentario"))
app.add_url_rule("/coments/<post_id>", view_func=ComentariosAPI.as_view("comentario_por_posteo"))
app.add_url_rule("/comentsModif/<coment_id>", view_func=ComentariosAPI.as_view("comentarios_modificados"))

### Rutas con templates:

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
        listaComentarios=coments,
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/principal", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        nombreCargado = request.form["usuarioActivo"]
        # uso la funcion filter_by porque con get solo puedo buscar por PK que es el id.
        usActivo = db.session.query(Usuario).filter_by(nombre=nombreCargado).first()

        # Lo paso como parametro en el render_template
        return render_template("main.html", UsAct=usActivo)


@app.route("/agregarUsuario", methods=["POST"])
def agregarUsuario():
    if request.method == "POST":
        nombreUsuario = request.form["usuario"]
        correoUsuario = request.form["correo"]
        contrasenaUsuario = request.form["contra"]

        nuevoUsuario = Usuario(
            nombre=nombreUsuario, correo=correoUsuario, contrasena=contrasenaUsuario
        )
        db.session.add(nuevoUsuario)
        db.session.commit()

        return redirect(url_for("index"))


@app.route("/comentarios", methods=["POST"])
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
        return render_template(
            "comentarios.html", enActiva=objetoEntrada, UsAct=usActivo
        )


@app.route("/usuarios")
def user():
    return render_template("users.html")


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

        # Id para carga de base de datos.
        cat = db.session.query(Categorias).all()
        etiquetaId = ""
        for cate in cat:
            if cate.nombre == etiquetaPost:
                etiquetaId = cate.id
        nuevoPost = Entrada(
            titulo=tituloPost,
            contenido=textoPost,
            fecha=fechaPost,
            autor=usuarioId,
            etiqueta=etiquetaId,
        )
        db.session.add(nuevoPost)
        db.session.commit()

        return render_template("main.html", UsAct=usActivo)


@app.route("/agregarComentario", methods=["GET", "POST"])
def agregarComentario():
    if request.method == "POST":
        fechaComent = request.form["fecha"]
        textoComent = request.form["texto"]
        usuarioId = request.form["idUsuario"]
        entradaId = request.form["idEntrada"]

        # entrada para cuando recargue la pagina.
        objetoEntrada = db.session.query(Entrada).filter_by(id=entradaId).first()

        # Id para carga de base de datos.
        usuBase = db.session.query(Usuario).all()
        usuNombre = ""
        for usuario in usuBase:
            if usuario.id == int(usuarioId):
                usActivo = usuario
        nuevoComent = Comentarios(
            contenido=textoComent,
            fecha=fechaComent,
            autor=usuarioId,
            etiqueta=entradaId,
        )
        db.session.add(nuevoComent)
        db.session.commit()

        return render_template(
            "comentarios.html", enActiva=objetoEntrada, UsAct=usActivo
        )
