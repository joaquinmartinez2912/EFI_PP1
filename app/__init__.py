import os

from flask import (Flask)

from dotenv import load_dotenv

from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')


db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

from app.views import view

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5006)
