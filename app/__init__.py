from flask import (Flask)

from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#mysql+pymysql://usuario:contraseña@ip/nombre_db
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/efi"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

from app.views import view

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
