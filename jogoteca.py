from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# importando token de segurança para os formulários
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

# Início da aplicação
app = Flask(__name__)

# pegando as configurações do arquivo config.py
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

# importando todas(*) as views: rotas e metodos
from views_game import *
from views_user import *

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=8080)
    # Fim da aplicação