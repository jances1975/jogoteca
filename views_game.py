# metodos do Flask
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
# O nosso proprio app do jogoteca.py
from jogoteca import app, db
# E as class Jogos e Usuários que movemos para o arquivo models.py
from models import Jogos
# Nesse arquivo helpers.py tem uma função que varre a pasta uploads buscando arquivo de imagem com id jogo
# importando a função deleta arquivos e a classe FormularioJogo que cria os formulários Flask-WTF
from helpers import recupera_imagem, deleta_arquivo, FormularioJogo
# Importando time para utilizar para criar arquivos de imagem com nomes úncos
import time

# Criando uma rota e a função da rota
@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', jogos=lista)
    # atribuimos a variavel lista uma query organizada pelo camo id da Tabela Jogos
    # Não precisa colocar o template/lista.html pois flask já utiliza a
    # pasta template como padrão

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    # Fazendo filtro com id que veio lista.html e mostrando o 1º registro do filtro
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo foi deletado!')
    return redirect(url_for('index'))

# Primeiro metodo editar que vai abrir uma página editar.html já com todos dados que serão alterados
# que virão da página lista.html onde trá um botão editar para todos os jogos
# id vem do lista.html do link: <th><a href="{{ url_for('editar', id=jogo.id) }}">Editar</a></th>
@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    # Fazendo filtro com id que veio lista.html e mostrando o 1º registro do filtro
    jogo = Jogos.query.filter_by(id=id).first()
    # Instanciando class FormularioJogo na variavel form para acessar os inputs
    form = FormularioJogo()
    # os inputs (form.nome.data) vão receber o seu campo da tabela (jogo.nome)
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    # função recupera_imagem(id) do arquivo helpers.py procura a imagem do jogo dentro pasta uploads
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando o Jogo', id=id, capa_jogo=capa_jogo, form=form)

# E o metodo atualizar que vai enviar do form da página editar.html que já fizemos as
# alterações para o BD e vai gravar
@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioJogo(request.form)
    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data
        db.session.add(jogo)
        db.session.commit()
        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        # capturando os segundos para usar no nome do arquivo da imagem p/ nunca tenha dois nomes de imagem iguais
        timestamp = time.time()
        deleta_arquivo(jogo.id)
        arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/novo')
def novo():
    if ('usuario_logado' not in session) or (session['usuario_logado'] == None):
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioJogo()
    return render_template('novo.html', titulo='Novo Jogo', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        flash('Jogo não foi gravado!')
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data
    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Esse jogo já existe!')
        return redirect(url_for('index'))
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()
    # Criando uma variável arquivo recebe requesição do template com input arquivo
    arquivo = request.files['arquivo']
    # Assim ele vai salvar a imagem com o nome capa+ID(código) do jogo.jpg
    # Isso para evitar que usuário grave jogo sempre com o mesmo nome: imagem.jpg
    # Pegando o path app config.py que tem uma variavel UPLOAD_PATH que possue:
    # path absoluto para a pasta uploads
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')
    # Salvando o arquivo na oasta uploads / nome do arquivo
    #arquivo.save(f'uploads/{arquivo.filename}')
    #return render_template('lista.html', titulo='Lista de Jogos', jogos=lista)
    return redirect(url_for('index'))


# importamos uma função Flask: send_from_directory
@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
    # A função Flask send_from_directory('pasta que esta a imagem', capa_padrao1.jpg)