# AAWZ Challenge Backend
Desafio técnico AAWZ - Backend

Esse README contêm respectivamente, os seguintes tópicos:
- Configuração de ambiente virtual venv (opcional, mas recomendado).
- Instalação de dependências
- Execução dos códigos

## Ambiente Virtual (Opcional, mas Recomendado)

Para isolar as dependências instaladas, é recomendado o uso de um ambiente virtual. Siga os passos abaixo para criar e ativar a venv:

### Linux e macOS

1. Abra o terminal.
2. Navegue até o diretório do projeto:

```bash
cd aawz_challenge
```

3. Crie um ambiente virtual:
```bash
python3 -m venv venv
```

4. Ative o ambiente virtual:
```bash
source venv/bin/activate
```

### Windows

1. Abra o prompt de comando
2. Navegue até o diretório do projeto:
```bash
cd aawz_challenge
```

3. Crie um ambiente virtual:
```bash
python3 -m venv venv
```

4. Ative o ambiente virtual:
```bash
venv\Scripts\activate
```

## Instalar Dependências
Para instalar as dependências, utilize o seguinte comando:
```bash
pip install -r requirements.txt
```

## Executando os códigos python

Para subir o backend, utilize o seguinte comando:
```bash
python3 app.py
```

A rota correspondente ao desafio n°1 é /vendedores.
É possível realizar requisições HTTP para essa rota pra fazer o CRUD.

A rota correspondente ao desafio n°2 é /importar_vendedores, eu implementei um html básico pra conseguir enviar um arquivo .CSV na requisição HTTP e conseguir testar mais facilmente essa tarefa. Exemplo de arquivo a ser utilizado [aqui](https://docs.google.com/spreadsheets/d/1dK91Yw69Wka9oA15Mw8zhz5GX3upiZihDyG14iZTAPg/edit?usp=sharing).



Segue anexo exemplo testando todas as possíveis requisições, utilizando PostMan:

to do
