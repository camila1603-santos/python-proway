# CÓDIGO PYTHON COMENTADO - SISTEMA DE GERENCIAMENTO DE CURSOS
# Este programa lê dados de cursos de um arquivo CSV, armazena em um banco SQLite
# e calcula estatísticas sobre os cursos

# ===== IMPORTAÇÃO DAS BIBLIOTECAS =====
import sqlite3  # Biblioteca para trabalhar com banco de dados SQLite
import csv      # Biblioteca para ler e escrever arquivos CSV
import os       # Biblioteca para trabalhar com caminhos de arquivos e sistema operacional

# ===== DEFINIÇÃO DOS CAMINHOS DOS ARQUIVOS =====
# __file__ é uma variável especial que contém o caminho do arquivo atual
# os.path.dirname(__file__) pega o diretório onde este script está localizado
# '..' significa "subir um nível" na estrutura de pastas
# os.path.join() junta os caminhos de forma segura (funciona em Windows, Linux, Mac)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db.sqlite3')
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'exercicios', 'cursos.csv')

# ===== 1. CONECTAR AO BANCO DE DADOS =====
# sqlite3.connect() cria uma conexão com o banco de dados
# Se o arquivo não existir, ele será criado automaticamente
conn = sqlite3.connect(DB_PATH)

# cursor é um objeto que permite executar comandos SQL no banco
# É como um "ponteiro" que navega pelo banco de dados
cursor = conn.cursor()

# ===== 2. CRIAR TABELA tb_cursos =====
# cursor.execute() executa um comando SQL
# CREATE TABLE IF NOT EXISTS significa: "crie a tabela apenas se ela não existir"
# Isso evita erros se executarmos o script várias vezes
cursor.execute('''
CREATE TABLE IF NOT EXISTS tb_cursos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Chave primária que incrementa automaticamente
    curso TEXT NOT NULL,                   -- Nome do curso (texto obrigatório)
    carga_horaria INTEGER NOT NULL,        -- Carga horária em horas (número inteiro obrigatório)
    preco REAL NOT NULL                    -- Preço do curso (número decimal obrigatório)
)
''')

# ===== 3. LER O ARQUIVO CSV E INSERIR OS DADOS =====
# 'with open()' é uma forma segura de abrir arquivos
# Quando o bloco termina, o arquivo é fechado automaticamente
# newline='' evita problemas com quebras de linha no CSV
# encoding='utf-8' garante que caracteres especiais (acentos) sejam lidos corretamente
with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    
    # List comprehension: uma forma compacta de criar listas
    # Para cada linha (row) do CSV, cria uma tupla com os dados
    # int() converte texto para número inteiro
    # float() converte texto para número decimal
    cursos = [(row['curso'], int(row['carga_horaria']), float(row['preco'])) for row in reader]

# ===== LIMPAR TABELA ANTES DE INSERIR =====
# DELETE FROM remove todos os registros da tabela
# Isso evita dados duplicados se executarmos o script várias vezes
cursor.execute('DELETE FROM tb_cursos')

# executemany() executa o mesmo comando SQL várias vezes
# Os '?' são placeholders (marcadores) que serão substituídos pelos valores
# Isso é mais seguro que concatenar strings (evita SQL injection)
cursor.executemany('INSERT INTO tb_cursos (curso, carga_horaria, preco) VALUES (?, ?, ?)', cursos)

# commit() confirma as alterações no banco de dados
# Sem isso, as mudanças ficam apenas na memória e são perdidas
conn.commit()

# ===== 4. CALCULAR ESTATÍSTICAS =====

# Contar quantos cursos existem na tabela
cursor.execute('SELECT COUNT(*) FROM tb_cursos')
# fetchone() retorna uma tupla com o resultado da consulta
# [0] pega o primeiro (e único) elemento da tupla
qtd_cursos = cursor.fetchone()[0]

# Encontrar o curso com maior carga horária
# ORDER BY carga_horaria DESC ordena por carga horária em ordem decrescente (maior primeiro)
# ORDER BY id ASC é um critério de desempate (se houver empate, pega o de menor ID)
# LIMIT 1 retorna apenas o primeiro resultado
cursor.execute('SELECT curso, carga_horaria FROM tb_cursos ORDER BY carga_horaria DESC, id ASC LIMIT 1')
curso_maior_carga = cursor.fetchone()

# Encontrar o curso com maior preço (mesma lógica do anterior)
cursor.execute('SELECT curso, preco FROM tb_cursos ORDER BY preco DESC, id ASC LIMIT 1')
curso_maior_valor = cursor.fetchone()

# ===== 5. CRIAR TABELA DE ESTATÍSTICAS =====
cursor.execute('''
CREATE TABLE IF NOT EXISTS tb_estatisticas_cursos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    qtd_cursos INTEGER,                    -- Quantidade total de cursos
    curso_maior_carga_horaria TEXT,        -- Nome e carga do curso com mais horas
    curso_com_maior_valor TEXT             -- Nome e preço do curso mais caro
)
''')

# Limpar tabela de estatísticas (mesmo motivo anterior)
cursor.execute('DELETE FROM tb_estatisticas_cursos')

# ===== 6. INSERIR ESTATÍSTICAS =====
cursor.execute(
    'INSERT INTO tb_estatisticas_cursos (qtd_cursos, curso_maior_carga_horaria, curso_com_maior_valor) VALUES (?, ?, ?)',
    (
        qtd_cursos,  # Quantidade de cursos
        # f-string: forma moderna de formatar strings em Python
        # curso_maior_carga[0] é o nome do curso, [1] é a carga horária
        f"{curso_maior_carga[0]} ({curso_maior_carga[1]} horas)",
        # :.2f formata o número com 2 casas decimais
        f"{curso_maior_valor[0]} (R$ {curso_maior_valor[1]:.2f})"
    )
)
# Confirma as alterações no banco
conn.commit()

# ===== 7. EXIBIR ESTATÍSTICAS NA TELA =====
# print() exibe informações no console/terminal
print(f"Quantidade de cursos: {qtd_cursos}")
print(f"Curso com a maior carga horária: {curso_maior_carga[0]} ({curso_maior_carga[1]} horas)")
print(f"Curso com o maior valor: {curso_maior_valor[0]} (R$ {curso_maior_valor[1]:.2f})")

# ===== FECHAR CONEXÃO COM O BANCO =====
# Sempre importante fechar a conexão para liberar recursos
conn.close()