from jogoteca import app
from flask import render_template, request, redirect, session, flash, url_for
from models import Usuarios
from helpers import FormularioUsuario, FormularioCadastroUsuario
from flask_bcrypt import check_password_hash


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario(request.form)
    return render_template('login.html', proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    # Vai filtra os os usuarios pelo nickname e retorna o primeiro do filtro
    # verificando se o usuario existe, se a variavel usuarios verdadeira ou seja existe algum usuario nela
    # a senha vai ser ma variavel bolean pois recebrera a confirmação se a senha do BD = Form
    senha = check_password_hash(usuario.senha, form.senha.data)
    # se usuario e senha forem iguais a True entra
    if usuario and senha:
        # verificando se senha que vem form/html == no dic estamos localizando pela chave usuario
        # quem vem do form/html quando lozalizar testar com .senha desse usuário
        # if request.form['senha'] == usuarios[request.form['usuario']].senha:
        # ou simplificando
        session['usuario_logado'] = usuario.nickname
        flash(usuario.nickname + ' logado com sucesso!')
        proxima_pagina = request.form['proxima']
        if proxima_pagina != 'None':
            return redirect(proxima_pagina)
        else:
            return redirect('/')
    else:
        flash("Usuário ou senha não reconhecidos!")
        return redirect(url_for('login'))
    # Antes erá assim fixo ao se agora vem dos dados da class:
    # if ('123' == request.form['senha']) and ('jances' == request.form['usuario']):

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuário deslogogado com sucesso!')
    return redirect(url_for('index'))

@app.route('/listauser')
def listauser():
    usuario = Usuarios.query.filter_by(nickname=session['usuario_logado']).first()
    user = Usuarios.superuser
    usuario.nickname
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Você não está logado!')
        return redirect(url_for('login', proxima=url_for('login', id=id)))
    if Usuarios.superuser == 's':
        listausers = Usuarios.query.order_by(Usuarios.nickname).all()
        return render_template('lista_usuarios.html', usuarios=listausers)
    else:
        flash(str(usuario.nickname)+' '+str(session['usuario_logado']))
        flash('Você está logado mas não tem acesso a lista de Usuários!')
        return redirect(url_for('index'))