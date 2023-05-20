from flask import render_template, redirect, url_for, flash, request, abort
from flaskwebsite import app, database, bcrypt
from flaskwebsite.forms import FormLogin, FormCriarConta, FormPesquisa
from flaskwebsite.models import Usuario, Webhook, Json
from flask_login import login_user, logout_user, login_required
import json


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/hooks")
@login_required
def hooks():
    lista_hooks = Webhook.query.order_by(Webhook.data_evento.desc()).limit(200).all()
    lista_teste = Json.query.all()
    return render_template('hooks.html', lista_hooks=lista_hooks, lista_teste=lista_teste)


@app.route("/pesquisa", methods=['GET', 'POST'])
@login_required
def pesquisa():
    form_pesquisa = FormPesquisa()
    if form_pesquisa.validate_on_submit():
        email_pesquisa = form_pesquisa.email.data.strip()
        resultados = Webhook.query.filter_by(email=email_pesquisa).all()
        if resultados:
            return render_template('resultado_pesquisa.html', resultados=resultados)
        else:
            flash('E-mail não encontrado na base de dados. Certifique-se de ter digitado corretamente.', 'alert-danger')
    return render_template('pesquisa.html', form=form_pesquisa)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit():  # fez login com sucesso
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login. E-mail e/ou senha incorretos.', 'alert-danger')
    return render_template('login.html', form_login=form_login)


@app.route("/criarconta", methods=['GET', 'POST'])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode("utf-8")
        usuario = Usuario(email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()

        login_user(usuario)

        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')

        return redirect(url_for('hooks'))
    return render_template('criarconta.html', form_criarconta=form_criarconta)


@app.route("/sair")
@login_required
def sair():
    logout_user()
    flash('Logout realizado com sucesso.', 'alert-secondary')
    return redirect(url_for('home'))


@app.route('/teste', methods=['POST'])
def webhook():
    # if request.method == 'POST':
    try:
        if request.is_json:
            # wh_data = request.json
            wh_data = request.get_json()
        else:
            wh_data = request.data.decode('utf-8')
            wh_data = json.loads(wh_data)

        # teste = Json(json=str(wh_data))

        nome = wh_data.get('nome')
        email = wh_data.get('email')
        email = email.lower()
        status = wh_data.get('status')

        if status == 'aprovado':
            print(f"Liberar acesso do e-mail: {email}")
            print(f"Bem-vindo, {nome}!")
            evento = f"✔️ Acesso liberardo para: {email} | Mensagem de boas-vindas enviada para {nome}."
        elif status == 'recusado':
            print(
                f"Olá {nome}! Ocorreu algum problema no pagamento. Revise os dados ou insira uma nova forma de pagamento.")
            evento = f"⚠️ Aviso de revisão da forma de pagamento enviado para {nome}."
        elif status == 'reembolsado':
            print("Acesso cancelado.")
            evento = "⛔ Acesso cancelado."
        else:
            evento = "Nenhuma ação tomada."

        wh = Webhook(nome=nome,
                     email=email,
                     status=status,
                     valor=wh_data['valor'],
                     forma_pagamento=wh_data['forma_pagamento'],
                     parcelas=wh_data['parcelas'],
                     evento=evento)
        database.session.add(wh)
        # database.session.add(teste)
        database.session.commit()
        return 'success', 200
    except Exception as e:
        abort(400, str(e))
