"""
Entrada e Saída(I/O) de arquivos em Python.

Leitura de arquivos .txt
"""

# Módulo com funções para trabalharmos com o sistema de arquivos do sistema operacional
import os

if __name__ == "__main__":

    """
    O método os.path.join concatena os caminhos informados até o arquivo. Essa é a melhor maneira de se evitar erros na hora de referenciar arquivos/pastas no sistema. Abaixo estamos concatenando o retorno da função os.getcwd() com a pasta "arquivos" e com o arquivos "linguagens.txt"
    """
    caminho_arquivo = os.path.join(os.getcwd(), "arquivos", "linguagens.txt")

    """
    Para abrir qualquer arquivos que seja, utilizamos a função built-in open. Essa função possui apenas 1 parâmetro obrigatório (file), que indica o caminho do arquivo que será aberto.

    O segundo parâmetro da função é o parâmetro mode, que indica o modo de abertura do arquivo. Caso não passemos um valor para esse parâmetro, por padrão o arquivo será aberto como um arquivo texto e somente-leitura. Caso queiramos ser mais explícitos, podemos passar o parâmetro mode de algumas maneira:
    
    open(caminho_arquivo, mode='r')     # Arquivo texto somente leitura (padrão)
    open(caminho_arquivo, mode='rt')     # Arquivo texto somente leitura (padrão)
    open(caminho_arquivo, mode='w')     # Arquivo texto somente escrita
    open(caminho_arquivo, mode='ab')    # Arquivo binário aberto para extensão

    E assim por diante...
    """

    # Como só passamos o parâmetro file, o arquivo será aberto como um arquivo texto e somente leitura. Caso o arquivo não exista, será lançada uma exceção FileNotFoundError
    arquivo = open(caminho_arquivo)

    # A função open retorna um objeto do tipo TextIOWrapper, que possui métodos e atributos. O método read lê o conteúdo completo do arquivo e retorna como uma string, inclusive mantendo os caracteres especiais, como tab e newline.
    print(arquivo.read())

    # Muito importante sempre fecharmos o arquivo depois do uso. Utilizamos o método close para fazer isso.
    arquivo.close()
    print('*'*50)

    # Abrindo o arquivo utilizando with. A vantagem dessa abordagem é que não precisamos chamar o método close de maneira explicita, pois no momento em que o bloco de código deixar de ser executado, o arquivo é automaticamente fechado.
    with open(caminho_arquivo, mode='tr') as arquivo:

        # O método read possui um parâmetro opcional chamado size, que nada mais é do que a quantidade de caracteres que queremos ler no arquivo.
        # Internamente, a posição de leitura é controlada pelo cursor. No caso abaixo, lemos os primeiros 5 caracteres do arquivo, e depois lemos os próximos 3 caracteres de onde o cursor parou
        print(arquivo.read(5))
        print(arquivo.read(3))

        # O método readline lê o conteúdo a partir do cursor até o final da linha. Esse método também possui um parâmetro opcional, que é a quantidade de caracteres que serão lidos
        print(arquivo.readline())

        # Mesmo que o parâmetro size seja maior que a quantidade de caracteres na linha, o método readline lê apenas os caractes na linha atual.
        print(arquivo.readline(20))

        # O método readlines() lê o conteúdo do arquivo e retorna as linhas como itens de uma lista
        print(arquivo.readlines())

        # Como o cursor está no final do arquivo, o método readlines() irá retornar uma lista vazia.
        print(arquivo.readlines(3))

        # Podemos consultar e alterar a posição atual do cursor com os métodos tell() e seek()
        print(arquivo.tell())

        arquivo.seek(0)

        # O parâmetro hint indica quantos caracteres serão lidos. Mesmo se o cursor pare antes do final da linha, o método lerá todos os caractes da linha
        print(arquivo.readlines(15))