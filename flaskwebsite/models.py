from flaskwebsite import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)


class Webhook(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    data_evento = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    nome = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False)
    status = database.Column(database.String, nullable=False)
    valor = database.Column(database.Float)
    forma_pagamento = database.Column(database.String)
    parcelas = database.Column(database.Integer)
    evento = database.Column(database.String)
    # id_aluno = database.Column(database.Integer, database.ForeignKey('aluno.id'), nullable=False)


class Json(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    json = database.Column(database.String)
