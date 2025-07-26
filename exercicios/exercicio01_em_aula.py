import pymysql #biblioteca para conexão com o banco de dados
import os #biblioteca para manipulação de arquivos
import requests #biblioteca para fazer requisições HTTP
from dotenv import load_dotenv #biblioteca para carregar variáveis de ambiente
import csv #biblioteca para manipulação de arquivos CSV

load_dotenv() #carrega as variáveis de ambiente

if __name__ == "__main__":
    pass #pass é uma instrução que não faz nada

    # Conexão com o banco de dados

    connection = pymysql.connect(
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST"), #corresponde a máquina local
        port=int(os.getenv("DATABASE_PORT")),
        database=os.getenv("DATABASE_NAME")
    )

    cursor = connection.cursor() #cursor é um objeto que permite executar comandos SQL

    url = "https://raw.githubusercontent.com/abispo/shared-files/refs/heads/main/modulo02/cursos.csv"

    response = requests.get(url) #faz uma requisição GET para a URL
    content = response.text #pega o conteúdo da resposta

    with open(os.path.join(os.getcwd(), "cursos.csv"), 'w', encoding='utf-8') as _file: #cria um arquivo CSV
        _file.write(content) #escreve o conteúdo no arquivo

    # Criação das tabelas
    command = """
    CREATE TABLE IF NOT EXISTS tb_cursos (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        curso VARCHAR(100) NOT NULL,
        carga_horaria INT NOT NULL,
        preco FLOAT NOT NULL
    );"""
    
    # Executa o comando SQL
    cursor.execute(command)

    command = """
    CREATE TABLE IF NOT EXISTS tb_estatisticas_cursos (
        id INT PRIMARY KEY AUTO_INCREMENT,
        qtd_cursos INT NOT NULL,
        curso_maior_carga_horaria VARCHAR(100) NOT NULL,
        curso_com_maior_valor VARCHAR(100) NOT NULL
    );"""
    cursor.execute(command)

    # Deletar os dados das tabelas para evitar duplicação
    cursor.execute("DELETE FROM tb_cursos")
    cursor.execute("DELETE FROM tb_estatisticas_cursos")
    connection.commit()

    with open(os.path.join(os.getcwd(), "cursos.csv"), 'r', encoding='utf-8') as _file:

        # DictReader: lê o arquivo CSV e retorna um dicionário

        csv_file = csv.DictReader(_file, delimiter=';')

        # Inserção dos dados no banco de dados para cada linha do arquivo CSV
        for row in csv_file:
            command = """
                INSERT INTO tb_cursos (curso, carga_horaria, preco) VALUES (
                '{}', {}, {}
                )""".format(
                    row.get("curso"),
                    int(row.get("carga_horaria")),
                    float(row.get("preco"))
                )
            cursor.execute(command)
        connection.commit()
    
    # Método 01: Utilizando o sql

    cursor.execute(
        "SELECT COUNT(*) FROM tb_cursos"
    )

    qtd_cursos = cursor.fetchone()[0]

    # Curso com maior carga horária
    cursor.execute(
        "SELECT * FROM tb_cursos ORDER BY carga_horaria DESC"
    )

    curso_maior_carga_horaria = cursor.fetchone()

    # Curso com maior valor
    cursor.execute(
        "SELECT * FROM tb_cursos ORDER BY preco DESC"
    )
    curso_com_maior_valor = cursor.fetchone()

    # Inserção das estatísticas no banco de dados
    command = """
    INSERT INTO tb_estatisticas_cursos (
        qtd_cursos, curso_maior_carga_horaria, curso_com_maior_valor) VALUES (
        {}, '{}', '{}'
        )""".format(
            qtd_cursos,
            f"{curso_maior_carga_horaria[1]} {curso_maior_carga_horaria[2]} horas",
            f"{curso_com_maior_valor[1]} (R$ {curso_com_maior_valor[3]})"
        )
    # Executa o comando SQL e salva as alterações no banco de dados
    cursor.execute(command)
    connection.commit()

    # Método 02: utilizando Python
    
    cursor.execute("SELECT * FROM tb_cursos")
    results = cursor.fetchall()

    qtd_cursos_2 = len(results)

    # sorted: ordena a lista de acordo com o valor da carga horária de forma decrescente e retorna o primeiro item
    # key: função que define o critério de ordenação
    # lambda: função anônima que define o critério de ordenação (item: item[2])
    # item: item[2] acessa o terceiro item da lista (carga horária)
    # reverse: True para ordenação decrescente
    # [0] retorna o primeiro item da lista ordenada
    curso_maior_carga_horaria_2 = sorted(
        results, key=lambda item: item[2], reverse=True)[0]

    # Curso com maior valor
    curso_com_maior_valor_2 = sorted(
        results, key=lambda item: item[3], reverse=True)[0]