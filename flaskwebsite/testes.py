from flaskwebsite import app, database
from flaskwebsite.models import Usuario, Webhook, Json

# with app.app_context():
#     database.drop_all()
#     database.create_all()

# with app.app_context():
#     hook1 = Webhook(nome="Nome do Aluno 3", email="email3@aluno.com", status="Status3", valor=300, forma_pagamento="Pagamento 3", parcelas=3, evento="print3")
#     hook2 = Webhook(nome="Nome do Aluno 2", email="email2@aluno.com", status="Status2", valor=200, forma_pagamento="Pagamento 2", parcelas=2, evento="print2")
#     hook3 = Webhook(nome="Nome do Aluno 1", email="email1@aluno.com", status="Status1", valor=100, forma_pagamento="Pagamento 1", parcelas=1, evento="print1")
#     database.session.add(hook1)
#     database.session.add(hook2)
#     database.session.add(hook3)
#     database.session.commit()

# with app.app_context():
#     teste1 = Json(json=str({
#         "nome": "Nome do Cliente",
#         "email": "exemplo@email.com",
#         "status": "aprovado",
#         "valor": 870,
#         "forma_pagamento": "paypal",
#         "parcelas": 4
#         }))
#     database.session.add(teste1)
#     database.session.commit()

# with app.app_context():
#     meus_alunos = Json.query.all()
#     i = 0
#     for aluno in meus_alunos:
#         print(meus_alunos[i].json)
#         i += 1

# { % if lista_teste %}
# { %
# for lista in lista_teste %}
# < p > {{lista.json}} < / p >
# { % endfor %}
# { % endif %}
