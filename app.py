import pandas as pd
import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from vendedor import db, Vendedor
from models import db, VendaOnline, VendaTelefone, VendaLojaFisica

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



@app.route('/importar-vendedores', methods=['POST'])
def importar_vendedores():
    """
    Importa dados de vendedores a partir de um arquivo CSV para adicionar ou atualizar em lote.

    O CSV deve conter as colunas: Nome, CPF, data_nascimento, email, estado.

    Returns:
        JSON: Mensagem de sucesso ou erro.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    
    try:
        data = pd.read_csv(file)
    except Exception as e:
        return jsonify({'error': 'Erro ao ler o arquivo CSV', 'details': str(e)}), 400

    required_columns = {'nome', 'cpf', 'data_nascimento', 'email', 'estado'}
    if not required_columns.issubset(set(data.columns)):
        return jsonify({'error': f'Colunas obrigatórias ausentes: {required_columns}'}), 400

    for i, row in data.iterrows():
        vendedor = Vendedor.query.filter_by(cpf=row['cpf']).first()
        if vendedor:
            vendedor.atualizar(
                nome=row['nome'],
                data_nascimento=row['data_nascimento'],
                email=row['email'],
                estado=row['estado']
            )
        else:
            Vendedor.criar(
                nome=row['nome'],
                cpf=row['cpf'],
                data_nascimento=row['data_nascimento'],
                email=row['email'],
                estado=row['estado']
            )

    return jsonify({'message': 'Dados dos vendedores importados com sucesso'}), 200

@app.route('/importar-vendedores', methods=['GET'])
def upload_vendedores():
    """
    Rota para renderizar o formulário de upload de arquivo HTML.

    Returns:
        HTML: Formulário de upload de arquivo.
    """
    return render_template('importar_vendedores.html')


@app.route('/calcula-comissao', methods=['POST'])
def calcula_comissao():
    """
    Calcula a comissão a partir de um arquivo CSV enviado na requisição.

    O CSV deve conter as colunas: Data da Venda, Valor da Venda, Custo da Venda, Canal de Venda, Nome do Vendedor.

    Returns:
        JSON: Mensagem de sucesso ou erro.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    
    try:
        df = pd.read_csv(file, parse_dates=['Data da Venda'])
    except Exception as e:
        return jsonify({'error': 'Erro ao ler o arquivo CSV', 'details': str(e)}), 400

    # Verifica se as colunas necessárias estão presentes
    required_columns = {'Data da Venda', 'Valor da Venda', 'Custo da Venda', 'Canal de Venda', 'Nome do Vendedor'}
    if not required_columns.issubset(set(df.columns)):
        return jsonify({'error': f'Colunas obrigatórias ausentes: {required_columns}'}), 400

    # Função auxiliar para retirar uma substring de uma string em uma coluna do dataframe
    def retira_string(df: pd.DataFrame, col: str, substr: str) -> pd.DataFrame:
        df[col] = df[col].str.replace(substr, '')
        return df

    # Função auxiliar para converter valores em formato "Real brasileiro" para float
    def reais_para_float(df: pd.DataFrame, col: str) -> pd.DataFrame:
        df = retira_string(df, col, 'R$ ')
        df[col] = df[col].str.replace('.', '')
        df[col] = df[col].str.replace(',', '.')
        df[col] = df[col].astype(float)
        return df

    # Transforma as colunas que representam Real brasileiro em formato número float
    df = reais_para_float(df, 'Valor da Venda')
    df = reais_para_float(df, 'Custo da Venda')

    # Calcula a comissão
    df['Comissao Total'] = df['Valor da Venda'] * 0.1
    df['Comissao Descontada'] = df['Comissao Total']

    # Ajustes para vendas online
    vendas_online = df['Canal de Venda'] == 'Online'
    df.loc[vendas_online, 'Comissao Descontada'] -= df.loc[vendas_online, 'Comissao Total'] * 0.2

    # Ajustes para comissões altas
    comissoes_altas = df['Comissao Total'] >= 1000
    df.loc[comissoes_altas, 'Comissao Descontada'] -= df.loc[comissoes_altas, 'Comissao Total'] * 0.1

    df_comissao = df[['Nome do Vendedor', 'Comissao Total', 'Comissao Descontada']]

    # Cria o diretório de dados de saída, caso ele não exista
    if not os.path.exists('output_data/'):
        os.makedirs('output_data/')

    # Gera o arquivo csv com a saída pedida
    output_file = 'output_data/Comissao_gerada.csv'
    df_comissao.to_csv(output_file, index=False)

    return jsonify({'message': 'Comissão calculada e arquivo gerado com sucesso', 'file_path': output_file}), 200

@app.route('/calcula-comissao', methods=['GET'])
def upload_comissao():
    """
    Rota para renderizar o formulário de upload de arquivo HTML.

    Returns:
        HTML: Formulário de upload de arquivo.
    """
    return render_template('calcula_comissao.html')



@app.route('/volume-vendas', methods=['POST'])
def volume_vendas():
    """
    Calcula o volume de vendas e a média por vendedor, recebendo um arquivo CSV enviado na requisição.
    O CSV deve conter as colunas: Data da Venda, Valor da Venda, Custo da Venda, Canal de Venda, Nome do Vendedor.
    Returns:
        JSON: Mensagem de sucesso ou erro.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    
    try:
        df = pd.read_csv(file, parse_dates=['Data da Venda'])
    except Exception as e:
        return jsonify({'error': 'Erro ao ler o arquivo CSV', 'details': str(e)}), 400

    # Verifica se as colunas necessárias estão presentes
    required_columns = {'Data da Venda', 'Valor da Venda', 'Custo da Venda', 'Canal de Venda', 'Nome do Vendedor'}
    if not required_columns.issubset(set(df.columns)):
        return jsonify({'error': f'Colunas obrigatórias ausentes: {required_columns}'}), 400

    # Função auxiliar para retirar uma substring de uma string em uma coluna do dataframe
    def retira_string(df: pd.DataFrame, col: str, substr: str) -> pd.DataFrame:
        df[col] = df[col].str.replace(substr, '')
        return df

    # Função auxiliar para converter valores em formato "Real brasileiro" para float
    def reais_para_float(df: pd.DataFrame, col: str) -> pd.DataFrame:
        df = retira_string(df, col, 'R$ ')
        df[col] = df[col].str.replace('.', '')
        df[col] = df[col].str.replace(',', '.')
        df[col] = df[col].astype(float)
        return df

    # Transforma as colunas que representam Real brasileiro em formato número float
    df = reais_para_float(df, 'Valor da Venda')
    df = reais_para_float(df, 'Custo da Venda')

    def agrupar_e_salvar(df: pd.DataFrame, canal: str, table) -> None:
        df_filtrado = df[df['Canal de Venda'] == canal]
        df_agrupado = df_filtrado.groupby('Nome do Vendedor', as_index=False).agg({'Valor da Venda': ['sum', 'mean']})
        df_agrupado.columns = ['Nome do Vendedor', 'Volume Total', 'Média']

        for _, row in df_agrupado.iterrows():
            venda = table(nome_do_vendedor=row['Nome do Vendedor'], volume_total=row['Volume Total'], media=row['Média'])
            db.session.add(venda)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': 'Erro ao salvar no banco de dados', 'details': str(e)}), 500

    agrupar_e_salvar(df, 'Online', VendaOnline)
    agrupar_e_salvar(df, 'Telefone', VendaTelefone)
    agrupar_e_salvar(df, 'Loja física', VendaLojaFisica)

    return jsonify({'message': 'Volume de vendas e média calculados e dados salvos com sucesso no banco de dados'}), 200


@app.route('/volume-vendas', methods=['GET'])
def upload_volume():
    """
    Rota para renderizar o formulário de upload de arquivo HTML.

    Returns:
        HTML: Formulário de upload de arquivo.
    """
    return render_template('volume_vendas.html')

if __name__ == '__main__':
    app.run(debug=True)



if __name__ == '__main__':
    app.run(debug=True)


