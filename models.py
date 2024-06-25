from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import re
import validate_cpf

db = SQLAlchemy()

class Vendedor(db.Model):
    """
    Classe que contêm o modelo de um vendedor.
    Os métodos dessa classe incluem todas as funções de um CRUD para gerenciar os Vendedores.

    Atributos:
        id (int): Identificador único do vendedor.
        nome (str): Nome do vendedor.
        cpf (str): CPF do vendedor, deve ser único.
        data_nascimento (str): Data de nascimento do vendedor.
        email (str): Email do vendedor.
        estado (str): Estado onde o vendedor reside.
    """
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    estado = db.Column(db.String(2), nullable=False)

    @classmethod
    def criar(cls, nome, cpf, data_nascimento, email, estado):
        """
        Cria um novo vendedor e o adiciona ao banco de dados.

        Args:
            nome (str): Nome do vendedor.
            cpf (str): CPF do vendedor.
            data_nascimento (str): Data de nascimento do vendedor.
            email (str): Email do vendedor.
            estado (str): Estado onde o vendedor reside.

        Returns:
            Vendedor: O objeto vendedor criado.
        """
        # Validação de email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email inválido")

        # Validação de CPF (apenas números e 11 dígitos)
        if not validate_cpf.is_valid(cpf):
            raise ValueError("CPF inválido")

        vendedor = cls(nome=nome, cpf=cpf, data_nascimento=data_nascimento, email=email, estado=estado)
        try:
            db.session.add(vendedor)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
        return vendedor

    @classmethod
    def ler(cls, vendedor_id=None):
        """
        Lê um ou todos os vendedores do banco de dados.

        Args:
            vendedor_id (int, opcional): O ID do vendedor para leitura. Se None, lê todos os vendedores.

        Returns:
            Vendedor ou list[Vendedor]: O vendedor com o ID fornecido ou a lista de todos os vendedores.
        """
        if vendedor_id:
            return cls.query.get(vendedor_id)
        return cls.query.all()

    def atualizar(self, **kwargs):
        """
        Atualiza os atributos do vendedor com os valores fornecidos.

        Args:
            **kwargs: Os atributos e seus novos valores.

        Returns:
            bool: True se a atualização for bem-sucedida, False caso contrário.
        """
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        try:
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def deletar(self):
        """
        Deleta o vendedor do banco de dados.

        Returns:
            bool: True se a exclusão for bem-sucedida, False caso contrário.
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def serializar(self):
        """
        Serializa o objeto Vendedor para um dicionário.

        Returns:
            dict: Dicionário contendo os dados do vendedor.
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'data_nascimento': self.data_nascimento,
            'email': self.email,
            'estado': self.estado
        }

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
