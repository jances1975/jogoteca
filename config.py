import os

# em vez de variavel normal: app.secret_key = 'alura'
# Criando uma variavel universal
SECRET_KEY = 'alura'

# Documentação Flask-SQLAlchemy: 'SGBD://usuario:senha@servidor/database'
#antes: app.config['SQLALCHEMY_DATABASE_URI'] = \
SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'admin',
        servidor = 'localhost',
        database = 'jogoteca'
    )

# Pegando o path raiz: os.path.abspath(__file__) de arquivo config.py
# O Caminho para diretorio que vamos passar como parametro: os.path.dirname()
# Nessa útima forma ele vai capturar o caminho completo até /uploads mesmo que esteje subpastas
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'