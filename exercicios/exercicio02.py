# CÓDIGO PYTHON COMENTADO - SISTEMA DE GERENCIAMENTO DE NOTAS
# Este programa gerencia notas de alunos, lendo-as de um CSV,
# armazenando-as em um banco de dados SQLite e calculando estatísticas.

# ===== IMPORTAÇÃO DE BIBLIOTECAS =====
# pathlib: Uma forma moderna e orientada a objetos de lidar com caminhos de arquivos e diretórios.
# É mais robusta e legível que o módulo 'os.path' para muitas operações.
from pathlib import Path

# sqlite3: Módulo padrão do Python para interagir com bancos de dados SQLite.
# SQLite é um banco de dados leve, baseado em arquivo, que não requer um servidor separado.
import sqlite3

# csv: Módulo para trabalhar com arquivos CSV (Comma Separated Values).
# Permite ler e escrever dados em formato tabular, onde os valores são separados por vírgulas (ou outros delimitadores).
import csv

# typing: Módulo que fornece suporte para type hints (dicas de tipo).
# Ajuda a escrever código mais claro e a detectar erros de tipo durante o desenvolvimento.
from typing import List, Tuple

# =====================================
# CONFIGURAÇÃO DE CAMINHOS DE ARQUIVOS
# =====================================
# BASE_DIR: Representa o diretório base onde este script está localizado.
# Path(__file__): Cria um objeto Path para o caminho completo deste arquivo Python.
# .resolve(): Resolve qualquer link simbólico e retorna o caminho absoluto e normalizado.
# .parent: Retorna o diretório pai do arquivo, ou seja, a pasta onde este script reside.
BASE_DIR = Path(__file__).resolve().parent

# EX_DIR: Representa o diretório 'exercicios' dentro do BASE_DIR.
# O operador '/' (barra) é sobrecarregado para objetos Path, permitindo concatenar caminhos de forma intuitiva.
EX_DIR = BASE_DIR / "exercicios"

# DB_PATH: Caminho completo para o arquivo do banco de dados SQLite.
# O banco de dados 'db.sqlite3' será criado dentro do diretório onde está este script.
DB_PATH = BASE_DIR / "db.sqlite3"

# CSV_PATH: Caminho completo para o arquivo CSV que contém as notas dos alunos.
# O arquivo 'notas.csv' também é esperado dentro do diretório onde está este script.
CSV_PATH = BASE_DIR / "notas.csv"

# =====================================
# SQL DE CRIAÇÃO DE TABELAS
# =====================================
# Definimos as instruções SQL como strings multi-linha para melhor legibilidade.

# CREATE_TB_NOTAS: SQL para criar a tabela 'tb_notas'.
# Esta tabela armazenará o nome do aluno e suas 5 notas.
CREATE_TB_NOTAS = """
CREATE TABLE IF NOT EXISTS tb_notas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 'id': Chave primária inteira que auto-incrementa para cada novo registro.
                                           -- Garante que cada aluno tenha um identificador único.
    nome TEXT NOT NULL,                    -- 'nome': Campo de texto para o nome do aluno. 'NOT NULL' significa que não pode ser vazio.
    nota1 REAL NOT NULL,                   -- 'nota1' a 'nota5': Campos de número real (ponto flutuante) para as notas.
    nota2 REAL NOT NULL,                   -- 'REAL' é usado para números decimais no SQLite.
    nota3 REAL NOT NULL,                   -- 'NOT NULL' garante que todas as notas sejam fornecidas.
    nota4 REAL NOT NULL,
    nota5 REAL NOT NULL
);
"""

# CREATE_TB_ESTATS: SQL para criar a tabela 'tb_estatisticas_notas'.
# Esta tabela armazenará estatísticas calculadas a partir das notas dos alunos.
# Note que não há 'id' explícito aqui, mas o SQLite adiciona um 'rowid' implícito para cada linha.
CREATE_TB_ESTATS = """
CREATE TABLE IF NOT EXISTS tb_estatisticas_notas (
    quantidade_de_alunos INTEGER NOT NULL, -- 'quantidade_de_alunos': Número total de alunos processados.
    media_geral REAL NOT NULL,             -- 'media_geral': Média das médias aparadas de todos os alunos.
    maior_media REAL NOT NULL,             -- 'maior_media': A maior média aparada encontrada entre os alunos.
    aluno_maior_media TEXT NOT NULL        -- 'aluno_maior_media': O nome do aluno que obteve a maior média aparada.
);
"""

# =====================================
# FUNÇÕES UTILITÁRIAS
# =====================================
# Funções que encapsulam lógicas específicas para reutilização e organização do código.

def load_csv_notas(path: Path) -> List[Tuple[str, float, float, float, float, float]]:
    """
    Lê o arquivo CSV de notas e retorna uma lista de tuplas.
    Cada tupla contém (nome, nota1, nota2, nota3, nota4, nota5).

    Args:
        path (Path): O objeto Path para o arquivo CSV de notas.

    Returns:
        List[Tuple[str, float, float, float, float, float]]: Uma lista de tuplas com os dados dos alunos.

    Raises:
        FileNotFoundError: Se o arquivo CSV não for encontrado.
        ValueError: Se o CSV não contiver as colunas esperadas ou se houver erro de conversão de tipo.
    """
    # Verifica se o arquivo CSV existe no caminho especificado.
    if not path.exists():
        # Se não existir, levanta uma exceção FileNotFoundError, informando o usuário.
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {path}")

    # Abre o arquivo CSV de forma segura usando 'with'.
    # 'newline=""': Importante para o módulo csv, evita problemas com quebras de linha.
    # 'encoding="utf-8"': Garante que caracteres especiais (acentos, cedilhas) sejam lidos corretamente.
    with path.open(newline="", encoding="utf-8") as f:
        # csv.DictReader: Cria um leitor que trata cada linha do CSV como um dicionário.
        # As chaves do dicionário são os nomes das colunas (do cabeçalho do CSV).
        # 'delimiter=";"': Especifica que o delimitador entre as colunas é o ponto e vírgula, não a vírgula padrão.
        # 'fieldnames=None': Indica que o DictReader deve inferir os nomes das colunas da primeira linha do CSV.
        reader = csv.DictReader(f, delimiter=";")

        # Define o conjunto de nomes de colunas esperados no CSV.
        required = {"nome", "n1", "n2", "n3", "n4", "n5"}
        # Verifica se o cabeçalho do CSV contém todas as colunas necessárias.
        if reader.fieldnames is None or not required.issubset(set(fn.lower() for fn in reader.fieldnames)):
            raise ValueError(f"O CSV deve conter as colunas: {required} (respeitando esses nomes).")

        rows = []
        for row in reader:
            try:
                nome = row["nome"]
                n1 = float(row["n1"])
                n2 = float(row["n2"])
                n3 = float(row["n3"])
                n4 = float(row["n4"])
                n5 = float(row["n5"])
            except KeyError as e:
                raise ValueError(f"Coluna ausente no CSV: {e}") from e
            except ValueError as e:
                raise ValueError(f"Não foi possível converter alguma nota para float. Linha: {row}") from e

            rows.append((nome, n1, n2, n3, n4, n5))
        return rows


def trimmed_mean_5_notas(notas: Tuple[float, float, float, float, float]) -> float:
    """
    Calcula a média aparada de 5 notas.
    A média aparada exclui a menor e a maior nota antes de calcular a média das restantes.

    Args:
        notas (Tuple[float, float, float, float, float]): Uma tupla contendo exatamente 5 notas (valores float).

    Returns:
        float: A média aparada das notas.

    Raises:
        ValueError: Se o número de notas não for exatamente 5.
    """
    # Verifica se a tupla 'notas' contém exatamente 5 elementos.
    if len(notas) != 5:
        # Se não, levanta um ValueError, pois a função é específica para 5 notas.
        raise ValueError("São esperadas exatamente 5 notas.")
    
    # sorted(notas): Cria uma nova lista com as notas ordenadas em ordem crescente.
    ordenadas = sorted(notas)
    
    # intermediarias = ordenadas[1:-1]: Seleciona todas as notas, exceto a primeira (menor) e a última (maior).
    # Isso efetivamente exclui a menor e a maior nota.
    intermediarias = ordenadas[1:-1]
    
    # sum(intermediarias): Soma as notas restantes.
    # len(intermediarias): Conta quantas notas restaram (sempre 3 neste caso).
    # Retorna a média das notas intermediárias.
    return sum(intermediarias) / len(intermediarias)


def calcular_estatisticas(cur) -> Tuple[int, float, float, str]:
    """
    Lê as notas da tabela tb_notas, calcula e retorna estatísticas gerais.

    Args:
        cur: O objeto cursor do SQLite, usado para executar comandos SQL.

    Returns:
        Tuple[int, float, float, str]: Uma tupla contendo:
            - quantidade_de_alunos (int)
            - media_geral (float): Média das médias aparadas de todos os alunos.
            - maior_media (float): A maior média aparada individual.
            - aluno_maior_media (str): O nome do aluno com a maior média aparada.
    """
    # Executa uma consulta SQL para selecionar o nome e todas as 5 notas de todos os alunos da tb_notas.
    cur.execute("""SELECT nome, nota1, nota2, nota3, nota4, nota5 FROM tb_notas""")
    # fetchall(): Recupera todas as linhas do resultado da consulta.
    # Cada linha é retornada como uma tupla.
    rows = cur.fetchall()

    # Calcula a quantidade total de alunos com base no número de linhas recuperadas.
    qtd = len(rows)
    
    # Verifica se não há alunos. Isso evita uma divisão por zero se a tabela estiver vazia.
    if qtd == 0:
        # Retorna valores neutros/zero para as estatísticas se não houver dados.
        return 0, 0.0, 0.0, ""

    medias_por_aluno = [] # Lista para armazenar tuplas (nome_aluno, media_aparada).
    # Itera sobre cada linha (tupla) de dados de aluno recuperada do banco de dados.
    for nome, n1, n2, n3, n4, n5 in rows:
        # Chama a função trimmed_mean_5_notas para calcular a média aparada das notas do aluno atual.
        media = trimmed_mean_5_notas((n1, n2, n3, n4, n5))
        # Adiciona o nome do aluno e sua média aparada à lista.
        medias_por_aluno.append((nome, media))

    # Calcula a média geral de todas as médias aparadas dos alunos.
    # sum(m for _, m in medias_por_aluno): Soma apenas as médias (o segundo elemento de cada tupla).
    media_geral = sum(m for _, m in medias_por_aluno) / qtd

    # Encontra o aluno com a maior média aparada.
    # max(..., key=lambda x: x[1]): Encontra o item máximo na lista 'medias_por_aluno'
    # usando como critério de comparação o segundo elemento da tupla (a média).
    aluno_maior_media, maior_media = max(medias_por_aluno, key=lambda x: x[1])

    # Retorna todas as estatísticas calculadas.
    return qtd, media_geral, maior_media, aluno_maior_media


def main():
    """
    Função principal que orquestra todo o fluxo do programa:
    1. Carrega dados do CSV.
    2. Conecta ao banco de dados SQLite.
    3. Cria as tabelas necessárias.
    4. Limpa e insere os dados das notas no banco.
    5. Calcula as estatísticas.
    6. Limpa e insere as estatísticas no banco.
    7. Exibe as estatísticas na tela.
    """
    # 1) Ler CSV: Chama a função para carregar as notas do arquivo CSV.
    notas = load_csv_notas(CSV_PATH)

    # 2) Conectar ao banco: Abre uma conexão com o banco de dados SQLite.
    # O uso de 'with' garante que a conexão será fechada automaticamente ao final do bloco.
    with sqlite3.connect(DB_PATH) as conn:
        # Obtém um objeto cursor para executar comandos SQL.
        cur = conn.cursor()

        # 3) Criar tabelas: Executa os comandos SQL para criar as tabelas de notas e estatísticas.
        # executescript() permite executar múltiplas instruções SQL separadas por ponto e vírgula.
        cur.executescript(CREATE_TB_NOTAS + CREATE_TB_ESTATS)

        # 4) Limpar e inserir em tb_notas:
        # Limpa todos os registros existentes na tabela tb_notas para evitar duplicidade em execuções repetidas.
        cur.execute("DELETE FROM tb_notas")
        # Insere os dados das notas lidos do CSV na tabela tb_notas.
        # executemany() é eficiente para inserir múltiplas linhas de uma vez.
        # Os '?' são placeholders para os valores que serão inseridos.
        cur.executemany(
            """INSERT INTO tb_notas (nome, nota1, nota2, nota3, nota4, nota5)
               VALUES (?, ?, ?, ?, ?, ?)""",
            notas
        )

        # 5) Calcular estatísticas: Chama a função para calcular as estatísticas gerais.
        qtd, media_geral, maior_media, aluno_maior_media = calcular_estatisticas(cur)

        # 6) Limpar e inserir em tb_estatisticas_notas:
        # Limpa todos os registros existentes na tabela tb_estatisticas_notas.
        cur.execute("DELETE FROM tb_estatisticas_notas")
        # Insere as estatísticas calculadas na tabela tb_estatisticas_notas.
        cur.execute(
            """INSERT INTO tb_estatisticas_notas
               (quantidade_de_alunos, media_geral, maior_media, aluno_maior_media)
               VALUES (?, ?, ?, ?)""",
            (qtd, media_geral, maior_media, aluno_maior_media)
        )

        # 7) Exibir estatísticas na tela:
        # Usa f-strings para formatar e imprimir as estatísticas de forma legível no console.
        # :.2f formata números de ponto flutuante com duas casas decimais.
        print(f"Quantidade de alunos: {qtd}")
        print(f"Média geral (excluindo menor e maior nota de cada aluno): {media_geral:.2f}")
        print(f"Maior média: {maior_media:.2f}")
        print(f"Aluno com a maior média: {aluno_maior_media}")

        # conn.commit(): Confirma todas as alterações feitas no banco de dados dentro do bloco 'with'.
        # Essencial para que as inserções e deleções sejam salvas permanentemente.
        conn.commit()


# Bloco de execução principal:
# Isso garante que a função main() seja chamada apenas quando o script é executado diretamente,
# e não quando é importado como um módulo em outro script.
if __name__ == "__main__":
    main()