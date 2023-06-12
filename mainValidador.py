from time import time
from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dataclasses import dataclass
from datetime import date, datetime
import requests
import cliente

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testeValidador.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route("/")
def index():
    return render_template('api.html')

@app.route('/validar/<int:valorRem>/<int:valorTrans>', methods=['POST'])
def receberTransacao(valorRem, valorTrans):

    if valorRem >= valorTrans:
        return 'pode' # PODE
    else:
        return 'nao pode' # NAO PODE





@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

app.run(host='0.0.0.0',port=5002, debug=True)