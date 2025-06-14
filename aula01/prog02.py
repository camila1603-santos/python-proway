# Tipos de dados em Python - data type

# STRINGS: textos ou cadeia de caracteres que podem possuir quarquer caracter.

# docstring: fazer uma anotação e depois consegue gerar um documento

if __name__ == "__main__":

    print("Strings podem ser definidas utilizando aspas duplas ou simples.")
    print('Também podemos utilizar aspas dentro de aspas, "dessa maneira".')
    print("Ou então utilizando \"marcações\t especiais\" \n pula linha.")
    print("""
Também podemos utilizar string multi linhas.
          Toda a formatação que for definida nessa string, será mantida caso ela seja impressa7
          no terminal      
        """)
    
# Para concatenar strings em Python podemos utilizar algumas abordagens:
    # 1- utilizar o sinal de +
    print("Olá! O curso é sobre " + "Python " + "e começa no" + " sábado.")

    # 2- utilizando o estilo antigo do Python 2 (hoje utilizamos o Python 3)
    print("Olá %s. Sua nota final foi de %f" % ("Barbara", 8.5,))

    # 3- utilizando o método format
    print("A prova final do curso {} será em {}".format("Java Web", "14/07/2025"))
    # Também podemos passar os nomes dos parâmetros que vão substituir os valores
    print("No dia {dia_inicial} foram processados {qtde_arquivos} arquivos.".format(dia_inicial="04/08/2025", qtde_arquivos=7490))

    # 4- utilizando f strings
    # Qualquer expressão válida em Python pode ser colocada dentro das chaves. Uma expressão é um conjunto de comando
    # que irão retornar um valor. No caso abaixo, utilizamos a estrutura if else junto com operadores lógicos
    # e aritiméticos para retornar um valor que será concatenado no restante da string.
    print(f"O resultado do cálculo é {'Positivo' if (5 + 10 * (15 / 3)) >= (14 + 3 / (5 ** 5)) else 'Negativo'}")
