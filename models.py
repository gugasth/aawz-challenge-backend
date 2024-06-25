from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class VendaOnline(db.Model):
    __tablename__ = 'venda_online'
    id = db.Column(db.Integer, primary_key=True)
    nome_do_vendedor = db.Column(db.String(100), nullable=False)
    volume_total = db.Column(db.Float, nullable=False)
    media = db.Column(db.Float, nullable=False)

class VendaTelefone(db.Model):
    __tablename__ = 'venda_telefone'
    id = db.Column(db.Integer, primary_key=True)
    nome_do_vendedor = db.Column(db.String(100), nullable=False)
    volume_total = db.Column(db.Float, nullable=False)
    media = db.Column(db.Float, nullable=False)

class VendaLojaFisica(db.Model):
    __tablename__ = 'venda_loja_fisica'
    id = db.Column(db.Integer, primary_key=True)
    nome_do_vendedor = db.Column(db.String(100), nullable=False)
    volume_total = db.Column(db.Float, nullable=False)
    media = db.Column(db.Float, nullable=False)
