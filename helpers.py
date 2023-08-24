import os

from flask import flash

from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField
# from wtforms import StringField, DateField, IntegerField, BooleanField, FloatField, EmailField, FileField, PasswordField

class FormularioJogo(FlaskForm):
    nome = StringField('Nome do Jogo: ', [validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoria: ', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console: ', [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    nickname = StringField('Usuario: ', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField(('Senha: ', [validators.DataRequired(), validators.Length(min=1, max=100)]))
    login = SubmitField('Login')

class FormularioCadastroUsuario(FlaskForm):
    nome = StringField('Digite seu nome com sobrenome: ', [validators.DataRequired(), validators.Length(min=1, max=8)])
    nickname = StringField('Usuario: ', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField(('Senha: ', [validators.DataRequired(), validators.Length(min=1, max=100)]))
    superuser = StringField(('Sper Usuário(s ou n): ', [validators.DataRequired(), validators.Length(min=1, max=1)]))
    cadastro = SubmitField('Cadastrar')

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo
    return 'capa_padrao1.jpg'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao1.jpg':
        # apagar o "arquivo".jpg, join(juntar/concatenar): caminho pasta upload + nome arquivo
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))

