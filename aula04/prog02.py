"""
Entrada e Saída(I/O) de arquivos em Python.

Escrita de arquivos .txt
"""

import os

from random import randint

if __name__ == "__main__":

    # O método zfill preenche a string com zeros a esquerda até alcançar a quantidade especificada de caracteres.
    numeros = [
        str(randint(0, 999999)).zfill(6),
        str(randint(0, 999999)).zfill(6),
        str(randint(0, 999999)).zfill(6),
        str(randint(0, 999999)).zfill(6),
        str(randint(0, 999999)).zfill(6)
    ]

    caminho_pasta_saida = os.path.join(os.getcwd(), "saida")

    # Verificamos se o caminho existe (pasta ou arquivo). Caso não exista, é criada uma pasta
    if not os.path.exists(caminho_pasta_saida):
        os.mkdir(caminho_pasta_saida)

    caminho_arquivo = os.path.join(caminho_pasta_saida, "numeros.txt")

    # Abaixo estamos abrindo o arquivo como texto somente escrita. Caso o arquivo não exista, ele será criado. Porém caso exista, o seu conteúdo será apagado e o novo conteúdo será escrito.
    # De preferência definimos o encoding do arquivo como utf-8, para evitar problemas de leitura em editores/sistemas diferentes
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        
        for numero in numeros:
            arquivo.write(f"{numero}\n")

    
    with open(caminho_arquivo, 'a', encoding='utf-8') as arquivo:
        
        conteudo_arquivo = [
            "\nNúmeros sortedos no concurso 111 da Loteria Federal\n",
            "01/10/2000\n"
        ]

        arquivo.writelines(conteudo_arquivo)