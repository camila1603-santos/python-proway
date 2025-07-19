"""
Entrada e Saída(I/O) de arquivos em Python.

Trabalhando com arquivos .csv (Comma Separated Value) no Python

Escrita de arquivos com csv.writer e csv.DictWriter
"""

import csv
import os

if __name__ == "__main__":

    lista_de_compras = [
        [1, "Banana", 1, 19.90],
        [2, "Abacaxi", 2, 9.90],
        [3, "Maçã", 10, 0.99],
        [4, "Uva", 2, 11.70],
        [5, "Manga", 2, 7.90]
    ]

    caminho_pasta_saida = os.path.join(os.getcwd(), "saida")

    if not os.path.exists(caminho_pasta_saida):
        os.mkdir(caminho_pasta_saida)

    caminho_arquivo = os.path.join(caminho_pasta_saida, "lista_de_compras.csv")

    with open(caminho_arquivo, 'w', encoding="utf-8", newline="") as arquivo:

        # De maneira semelhante ao csv.reader, o csv.writer trabalha com linhas. Ou seja, se quisermos escrever no arquivo, precisamos definir a linha que será escrita
        arquivo_csv = csv.writer(arquivo, delimiter=';')

        # É aí que entra o método writerow. Ele irá receber uma lista de valores e irá escrever no arquivo, utilizando o caractere separador definido para separar os valores.
        arquivo_csv.writerow(["id", "produto", "quantidade", "valor"])

        # O método writerows espera um iterável que contenha outros iteráveis como itens. Esses itens podem conter qualquer valor
        arquivo_csv.writerows(lista_de_compras)

    nova_lista_de_compras = [
        {"id": 1, "produto": "Sabonete", "quantidade": 5, "valor_unitario": 1.29},
        {"id": 2, "produto": "Sabão em Pó", "quantidade": 2, "valor_unitario": 9.58},
        {"id": 3, "produto": "Pasta de Dente", "quantidade": 1, "valor_unitario": 5.14},
        {"id": 4, "produto": "Sabão em Pedra", "quantidade": 10, "valor_unitario": 3.17},
        {"id": 5, "produto": "Pregador", "quantidade": 2, "valor_unitario": 1.98},
    ]

    caminho_novo_arquivo = os.path.join(
        caminho_pasta_saida, "nova_lista_de_compras.csv"
    )

    with open(caminho_novo_arquivo, "w", encoding="utf-8", newline="") as arquivo:

        # Aqui utilizamos o csv.DictWriter, que assim como o DictReader, trabalha com dicionários. Também podemos indicar o parâmetro fieldnames, que serão os nomes das colunas do arquivo .csv
        arquivo_csv = csv.DictWriter(
            arquivo,
            delimiter=';',
            fieldnames=("id", "produto", "quantidade", "valor_unitario",)
        )

        # O método writeheader() escreve no arquivo as colunas que foram definidas no parâmetro fieldnames da classe csv.DictWriter
        arquivo_csv.writeheader()

        # O método writerows recebe uma lista de dicionários, onde cada dicionário representa uma linha que será escrita no arquivo.
        arquivo_csv.writerows(nova_lista_de_compras)

        # E por fim, o método writerow recebe um dicionário, que será escrito no arquivo
        arquivo_csv.writerow({
            "id": 6,
            "produto": "Fio Dental",
            "quantidade": 1,
            "valor_unitario": 3.14
        })