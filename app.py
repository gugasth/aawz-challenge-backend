from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from vendedor import db, Vendedor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aawz-challenge.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa a aplicação com a instância do banco de dados
db.init_app(app)

# Cria todas as tabelas no banco de dados se elas ainda não existirem
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    """
    Rota inicial que retorna uma mensagem de boas-vindas.

    Returns:
        str: Mensagem de boas-vindas.
    """
    return "Hello World!"

@app.route('/vendedores', methods=['POST'])
def criar_vendedor():
    """
    Cria um novo vendedor.

    Verifica se os dados fornecidos estão completos e se o CPF e o email já estão cadastrados no banco de dados.
    Se o CPF ou email já existirem, retorna um erro 400. Caso contrário, cria um novo vendedor e retorna o ID do novo registro.

    Requisição JSON:
        {
            "nome": "Nome do Vendedor",
            "cpf": "CPF do Vendedor",
            "data_nascimento": "Data de Nascimento",
            "email": "Email do Vendedor",
            "estado": "Estado do Vendedor"
        }

    Returns:
        JSON: ID do novo vendedor se criado com sucesso, ou uma mensagem de erro se os dados estiverem incompletos ou o CPF ou email já existirem.
    """
    data = request.get_json()
    if not data.get('nome') or not data.get('cpf') or not data.get('data_nascimento') or not data.get('email') or not data.get('estado'):
        return jsonify({'Erro': 'Dados incompletos'}), 400

    # Verifica se o CPF já existe no banco de dados
    cpf_existente = Vendedor.query.filter_by(cpf=data['cpf']).first()
    if cpf_existente:
        return jsonify({'Erro': 'CPF já cadastrado'}), 400

    # Verifica se o email já existe no banco de dados
    email_existente = Vendedor.query.filter_by(email=data['email']).first()
    if email_existente:
        return jsonify({'Erro': 'Email já cadastrado'}), 400

    vendedor = Vendedor.criar(**data)
    return jsonify({'id': vendedor.id}), 201

@app.route('/vendedores', methods=['GET'])
@app.route('/vendedores/<int:vendedor_id>', methods=['GET'])
def ler_vendedor(vendedor_id=None):
    """
    Lê um ou todos os vendedores do banco de dados.

    Args:
        vendedor_id (int, opcional): O ID do vendedor para leitura. Se None, lê todos os vendedores.

    Returns:
        JSON: Os dados do vendedor com o ID fornecido ou a lista de todos os vendedores.
    """
    if vendedor_id:
        vendedor = Vendedor.ler(vendedor_id)
        if vendedor:
            return jsonify(vendedor.serializar()), 200
        return jsonify({'error': 'Vendedor não encontrado'}), 404
    else:
        vendedores = Vendedor.ler()
        return jsonify([v.serializar() for v in vendedores]), 200

@app.route('/vendedores/<int:vendedor_id>', methods=['PUT'])
def atualizar_vendedor(vendedor_id):
    """
    Atualiza os dados de um vendedor específico.

    Args:
        vendedor_id (int): O ID do vendedor a ser atualizado.

    Requisição JSON:
        {
            "nome": "Novo Nome",
            "cpf": "Novo CPF",
            "data_nascimento": "Nova Data de Nascimento",
            "email": "Novo Email",
            "estado": "Novo Estado"
        }

    Returns:
        JSON: Os dados atualizados do vendedor, ou uma mensagem de erro se o vendedor não for encontrado.
    """
    data = request.get_json()
    vendedor = Vendedor.ler(vendedor_id)
    if not vendedor:
        return jsonify({'error': 'Vendedor não encontrado'}), 404

    vendedor.atualizar(**data)
    return jsonify(vendedor.serializar()), 200

@app.route('/vendedores/<int:vendedor_id>', methods=['DELETE'])
def deletar_vendedor(vendedor_id):
    """
    Deleta um vendedor específico.

    Args:
        vendedor_id (int): O ID do vendedor a ser deletado.

    Returns:
        JSON: Mensagem de sucesso ou erro se o vendedor não for encontrado.
    """
    vendedor = Vendedor.ler(vendedor_id)
    if not vendedor:
        return jsonify({'error': 'Vendedor não encontrado'}), 404

    vendedor.deletar()
    return jsonify({'message': 'Vendedor deletado com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True)
