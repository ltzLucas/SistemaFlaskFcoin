from collections import Counter
from random import random
from time import time
from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dataclasses import dataclass
from datetime import date, datetime
import requests
import cliente
import random
import time

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testeSeletor12.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@dataclass
@dataclass
class Validador(db.Model):
    id: int
    nome: str
    ip: int
    flag: int
    FCoins: int
    percent: int
    transacoes: int
    aux_flag: int

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    ip = db.Column(db.String(50), unique=False, nullable=False)
    flag = db.Column(db.Integer, unique=False, nullable=False)
    FCoins = db.Column(db.Integer, unique=False, nullable=False)
    percent = db.Column(db.Integer, unique=False, nullable=False)
    transacoes = db.Column(db.Integer, unique=False, nullable=False)
    aux_flag = db.Column(db.Integer, unique=False, nullable=False)

@dataclass
class MeuSeletor(db.Model):
    id: int
    fCoins: int
    qtd_transacoes: int

    id = db.Column(db.Integer, primary_key=True)
    fCoins = db.Column(db.Integer, unique=False, nullable=False)
    qtd_transacoes = db.Column(db.Integer, unique=False, nullable=False)


@app.route("/")
def index():
    return render_template('api.html')

def inicializarSeletor():
    objeto = MeuSeletor(fCoins=0,qtd_transacoes=0)
    db.session.add(objeto)
    db.session.commit()

@app.route('/meuSeletor', methods=['GET'])
def Seletor():
    if (request.method == 'GET'):
        seletor = MeuSeletor.query.all()
        return jsonify(seletor)

@app.route('/meuSeletor/<int:id>', methods=['DELETE'])
def ApagarMeuSeletor(id):
    if (request.method == 'DELETE'):
        objeto = MeuSeletor.query.get(id)
        db.session.delete(objeto)
        db.session.commit()

        data = {
            "message": "meuSeletor Deletado com Sucesso"
        }
        return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/validador', methods=['GET'])
def ListarCliente():
    if (request.method == 'GET'):
        clientes = Validador.query.all()
        return jsonify(clientes)

@app.route('/validador/<string:nome>/<string:ip>/<int:FCoins>', methods=['POST'])
def Cadastro_dos_Validadores(nome, ip,FCoins):
    if request.method == 'POST' and nome != '' and ip != '' and FCoins >= 100:
        objeto = Validador(nome=nome, ip=ip,flag=0,FCoins=FCoins,percent=0,transacoes=0,aux_flag=1)
        db.session.add(objeto)
        db.session.commit()

        calcular_percent()
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

def calcular_percent():
    validadores = Validador.query.all()
    meuSeletor = MeuSeletor.query.filter_by(id=1).first()

    totalFCoins = 0
    for v in validadores:
        totalFCoins += v.FCoins
    meuSeletor.fCoins = totalFCoins
    db.session.commit()

    for v in validadores:
        percentual = int((v.FCoins / meuSeletor.fCoins) * 100)
        if percentual < 5:
            percent = 5
        elif percentual > 40:
            percent = 40
        else:
            percent = percentual

        validadorObjeto = Validador.query.filter_by(id=v.id).first()
        db.session.commit()
        validadorObjeto.percent = percent
        db.session.commit()
        # print(f'Validador {v.id} está com o percentual de {percent}')


@app.route('/validador/<int:id>', methods=['GET'])
def UmSeletor(id):
    if (request.method == 'GET'):
        produto = Validador.query.get(id)
        return jsonify(produto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/validador/<int:id>', methods=['DELETE'])
def ApagarValidador(id):
    if (request.method == 'DELETE'):
        objeto = Validador.query.get(id)
        meuSeletor = MeuSeletor.query.filter_by(id=1).first()

        meuSeletor.fCoins -= objeto.FCoins
        db.session.commit()
        db.session.delete(objeto)
        db.session.commit()

        data = {
            "message": "Validador Deletado com Sucesso"
        }
        return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/transacao/<int:id>/<int:remetente>/<int:recebedor>/<int:valor>/<int:status>', methods=['POST'])
def receberTransacao(id,remetente,recebedor,valor,status):
    if request.method == 'POST':
        Validadores = Validador.query.all()
        rem = cliente.visualizar_Cliente_id(remetente)

        escolhidos = escolhe_validadores()

        saldoRem = rem['qtdMoeda']
        resultado_json = []
        for v in Validadores:
            for e in escolhidos:
                if v.id == e:
                    url = f'http://{v.ip}/validar/{v.id}/{saldoRem}/{valor}'
                    response = requests.post(url)
                    resultado_json.append(response.json())


        print(resultado_json)

        status_counts = Counter(item['status'] for item in resultado_json)

        most_common_status = status_counts.most_common(1)[0][0]

        print(f"O valor de status que mais aparece é: {most_common_status}")

        ids_with_different_status = [item['id'] for item in resultado_json if item['status'] != most_common_status]
        ids_with_same_status = [item['id'] for item in resultado_json if item['status'] == most_common_status]
        print(f"IDs com valores de status diferentes da maioria: {ids_with_different_status}")
        print(f"IDs com valores de status igauis da maioria: {ids_with_same_status}")

        #PARA QUEM ACERTOU A TRANSACAO adiciona +1
        for same_ids in ids_with_same_status:
            adicionar_transacao(same_ids)
            #TIRA FLAG CASO ELE TENHA ALGUMA E TRANSACOES SEJA >= 10000
            tirar_flag(same_ids)

        #ADICIONA UMA FLAG PRA QUEM ERROU A TRANSACAO
        for different_ids in ids_with_different_status:
            #ADICIONA UMA FLAG E CASO SEJA A TERCEIRA ELE É DELETADO DA REDE
            adicionar_flag(different_ids)

        return 'retorno mainSeletor transacao'
    else:
        return jsonify(['Method Not Allowed'])

def escolhe_validadores():
    Validadores = Validador.query.all()

    if len(Validadores) < 3:
        print('Transação em espera aguarde 1 min')
        time.sleep(60)
        Validadores = Validador.query.all()
        if len(Validadores) < 3:
            print('Não foi possivel concluir a transação por falta de validadores')
            return  0
    if len(Validadores) >= 5:
        escolhidos = cinco_validadores()
        print(f'5 ou mais validadores os escolhidos sao:  {escolhidos}')
        return  escolhidos
    elif len(Validadores) == 3 or len(Validadores) == 4:
        escolhidos = tres_validadores()
        print(f'3 ou 4 validadores os escolhidos sao:  {escolhidos}')
        return escolhidos

def adicionar_transacao(id):
    validadorObjeto = Validador.query.filter_by(id=id).first()
    db.session.commit()
    validadorObjeto.transacoes += 1
    db.session.commit()

def adicionar_flag(id):
    validadorObjeto = Validador.query.filter_by(id=id).first()
    db.session.commit()
    validadorObjeto.flag += 1
    db.session.commit()
    #Verifica quantas flags tem caso flags > 2 ele é deletado
    verifica_qtd_flags(id)

def verifica_qtd_flags(id):
    validadorObjeto = Validador.query.filter_by(id=id).first()
    db.session.commit()
    if validadorObjeto.flag > 2:
        objeto = Validador.query.get(id)
        db.session.delete(objeto)
        db.session.commit()
def tirar_flag(id):
    validadorObjeto = Validador.query.filter_by(id=id).first()
    db.session.commit()
    # ---------------------------------------------ARRUMAR 10000 TRANSACOES------------------------------------------
    if validadorObjeto.flag > 0 and validadorObjeto.transacoes >= 10 * validadorObjeto.aux_flag:
        validadorObjeto.flag -= 1
        validadorObjeto.aux_flag += 1
        db.session.commit()

def cinco_validadores():
    Validadores = Validador.query.all()
    validadoresID = []
    pesos = []

    escolhidos = tres_validadores()

    for v in Validadores:
        if v.id != escolhidos[0] and v.id != escolhidos[1] and v.id != escolhidos[2]:
            validadoresID.append(v.id)
            pesos.append(v.percent)

    v4 = random.choices(validadoresID, pesos)[0]
    # limpa as listas
    validadoresID.clear()
    pesos.clear()

    escolhidos.append(v4)

    for v in Validadores:
        if v.id != escolhidos[0] and v.id != escolhidos[1] and v.id != escolhidos[2] and v.id != v4:
            validadoresID.append(v.id)
            pesos.append(v.percent)

    v5 = random.choices(validadoresID, pesos)[0]
    escolhidos.append(v5)

    return escolhidos
def tres_validadores():
    Validadores = Validador.query.all()
    validadoresID = []
    pesos = []
    for v in Validadores:
        validadoresID.append(v.id)
        pesos.append(v.percent)

    v1 = random.choices(validadoresID, pesos)[0]
    # limpa as listas
    validadoresID.clear()
    pesos.clear()

    for v in Validadores:
        if v.id != v1:
            validadoresID.append(v.id)
            pesos.append(v.percent)

    v2 = random.choices(validadoresID, pesos)[0]
    # limpa as listas
    validadoresID.clear()
    pesos.clear()
    for v in Validadores:
        if v.id != v1 and v.id != v2:
            validadoresID.append(v.id)
            pesos.append(v.percent)

    v3 = random.choices(validadoresID, pesos)[0]
    # limpa as listas
    validadoresID.clear()
    pesos.clear()
    for v in Validadores:
        if v.id != v1 and v.id != v2 and v.id != v3:
            validadoresID.append(v.id)
            pesos.append(v.percent)

    escolhidos = [v1, v2, v3]

    return escolhidos

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        #LIGAR APENAS UMA VEZ PARA CRIAR UM SELETOR APENAS
        #inicializarSeletor()

app.run(host='0.0.0.0',port=5001, debug=True)