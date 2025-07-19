"""
Python com banco de dados

Assim como em outras linguagens, podemos utilizar o Python para acesso a vários tipos de banco de dados. Isso é feito
utilizando uma biblioteca de acesso, que também podemos chamar de conector. Através dessa biblioteca é definido e enviado
os comandos SQL que serão executados no bd.

Padrão: biblioteca que permite trabalhar com bd SQLite

"""


import os
import sqlite3

if __name__ == "__main__":
    
    """
    Geralmente quando queremos conectar nossa app a um banco de dados, seguimos o seguinte passo a passo:

    1. definimos a connection string do banco. É um texto com as informações necessárias para acessar o banco de dados: user, senha,
    endereço e etc.

    2. criamos uma conexão com o bando de dados a partir da connection string

    3. a partir da conexão, criamos um cursor. É através do cursor que enviamos os comandos sql para o banco de dados.

    4. executamos o cursor e se necessário pegamos o resultado do comando no bd.

    """

    # 1. Definir a connection string

    connection_string = os.path.join(os.getcwd(), "db.sqlite3")

    # 2. Criamos a conexão com o banco utilizando a connection string

    connection = sqlite3.connect(connection_string)

    # 3. Criação do cursor que será utilizado para executar os comandos SQL

    cursor = connection.cursor()

    # Nesse momento, já podemos utilizar o cursor para executar os comandos
    # Criando a tabela tb_cursos

    comando = """
        CREATE TABLE IF NOT EXISTS tb_cursos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL
        );
"""
    # 4. Executamos o comando definido anteriormente utilizando o cursor
    response = cursor.execute(comando)

    lista_cursos = [
        {"nome": "Fundamentos Python", "preco": 550},
        {"nome": "Java Avançado", "preco": 1500},
        {"nome": "Microserviços com Go", "preco": 990},
        {"nome": "Introdução ao DevOps", "preco": 600},
        {"nome": "Linux Básico", "preco": 750},
]

for curso in lista_cursos:
    comando = "INSERT INTO tb_cursos(nome, preco) VALUES ('{nome}', {preco})".format(
        **curso
    )

# Apenas o método execute() não irá salvar os dados na tabela. No caso de comandos DML (Data Manipulation Language)
# INSERT, DELETE e UPDATE precisamos confirmar a transação para que os dados sejam salvos. Nesse caso precisamos executar
# o método commit() da conexão, que irá confirmar essa transação.
    #cursor.execute(comando)

# Confirmação da transação
#connection.commit()

# CONSULTAR DADOS DA TABELA

# Método 01: fetchone(): retorna apenas um registro da tabela. Se a consulta não tiver resultados retorna none. Caso
# haja resultados , esse método retorna uma tupla, onde cada item da tupla é o valor da coluna.

command = "SELECT * FROM tb_cursos;"
cursor.execute(command)
response = cursor.fetchone()

print(response)

# Método 02: fetchmany(): retorna a quantidade de registros que é informada. Se a consulta não trouxer resultados,
# retorna uma lista vazia.

response = cursor.fetchmany(2)
print(response)

# Método 03: fetchall(): retorna todos os resultados da consulta. Se a consulta não trouxer resultados, retorna lista vazia.

response = cursor.fetchall()
print(response)

print(cursor.fetchall())

# 5.Fechamos o cursor e a conexão
cursor.close()
connection.close()