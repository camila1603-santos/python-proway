"""
Entrada e Saída(I/O) de arquivos em Python.

Trabalhando com arquivos .csv (Comma Separated Value) no Python

Leitura de arquivos com csv.reader e csv.DictReader
"""

import csv
import os

def formata_saida(
        first_name: str,
        last_name: str,
        birth_date: str,
        email: str,
        password: str = "",
        gender: str = "",
        id: str = "",
        username: str = ""
    ):
    
    print(f"{'Nome'.ljust(21)} {first_name} {last_name}")
    print(f"{'Data de Nascimento'.ljust(21)} {birth_date}")
    print(f"{'Email'.ljust(21)} {email}")
    print('-'*50)

if __name__ == "__main__":

    caminho_arquivo = os.path.join(os.getcwd(), "arquivos", "usuarios.csv")

    with open(caminho_arquivo, mode='r', encoding="utf-8") as arquivo:
        
        # Após abrir o arquivo texto, temos que gerar o objeto que irá representar o arquivo csv. Podemos utilizar csv.reader ou csv.DictReader. No caso do csv.reader, a cada iteração no arquivo csv, será retornada uma lista, com os valores sendo itens dessa lista.
        # Como o caractere separador padrão é a vírgula, temos que indicar o caractere caso não utilizemos o padrão. No caso do arquivo usuarios.csv, o caractere separador é o ponto-e-vírgula que indicamos no parâmetro delimiter
        arquivo_csv = csv.reader(arquivo, delimiter=';')

        # Não temos acesso aos métodos de leitura no arquivo .csv como temos quando trabalhamos com um arquivo .txt comum. Nesse caso, temos que iterar sobre o arquivo, e cada linha será retornada como uma lista de strings.
        for linha in arquivo_csv:
            print(f"{linha[2]} {linha[3]}")

        
        with open(caminho_arquivo, 'r', encoding="utf-8") as arquivo:

            # Utilizando o csv.DictReader
            arquivo_csv = csv.DictReader(arquivo, delimiter=';')

            # Diferentemente do csv.reader, o csv.DictReader retorna um dicionário a cada iteração. As chaves serão os valores da primeira linha, e os valores serão os valores da segunda linha em diante
            print(arquivo_csv.fieldnames)
            for linha in arquivo_csv:
                formata_saida(**linha)