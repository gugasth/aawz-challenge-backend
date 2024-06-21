from flask import Flask, request, jsonify
from vendedores import Vendedores

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello World!"


@app.route('/vendedores', methods=['POST'])
def criar_vendedor():
    data = request.get_json()
    vendedor = Vendedores.criar(
        nome=data.get('nome'),
        cpf=data.get('cpf'),
        data_nascimento=data.get('data_nascimento'),
        email=data.get('email'),
        estado=data.get('estado')
    )
    return jsonify({'id': vendedor.id}), 201

@app.route('/vendedores', methods=['GET'])
@app.route('/vendedores/<int:vendedor_id>', methods=['GET'])
def ler_vendedor(vendedor_id=None):
    if vendedor_id:
        vendedor = Vendedores.ler(vendedor_id)
        if vendedor:
            # Retorna JSON contêndo os atributos do vendedor
            return jsonify({
                'id': vendedor.id,
                'nome': vendedor.nome,
                'cpf': vendedor.cpf,
                'data_nascimento': vendedor.data_nascimento,
                'email': vendedor.email,
                'estado': vendedor.estado
            })
        return jsonify({'error': 'Vendedor não encontrado'}), 404
    else:
        # Retorna todos os vendedores
        vendedores = Vendedores.ler()
        return jsonify([{
            'id': vendedor.id,
            'nome': vendedor.nome,
            'cpf': vendedor.cpf,
            'data_nascimento': vendedor.data_nascimento,
            'email': vendedor.email,
            'estado': vendedor.estado
        } for vendedor in vendedores])

@app.route('/vendedores/<int:vendedor_id>', methods=['PUT'])
def atualizar_vendedor(vendedor_id):
    data = request.get_json()
    vendedor = Vendedores.atualizar(
        vendedor_id,
        nome=data.get('nome'),
        cpf=data.get('cpf'),
        data_nascimento=data.get('data_nascimento'),
        email=data.get('email'),
        estado=data.get('estado')
    )
    if vendedor:
        return jsonify({
            'id': vendedor.id,
            'nome': vendedor.nome,
            'cpf': vendedor.cpf,
            'data_nascimento': vendedor.data_nascimento,
            'email': vendedor.email,
            'estado': vendedor.estado
        })
    return jsonify({'error': 'Vendedor não encontrado'}), 404

@app.route('/vendedores/<int:vendedor_id>', methods=['DELETE'])
def deletar_vendedor(vendedor_id):
    vendedor = Vendedores.deletar(vendedor_id)
    if vendedor:
        return jsonify({'message': 'Vendedor deletado com sucesso'})
    return jsonify({'error': 'Vendedor não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)