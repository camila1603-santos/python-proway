"""
FUNÇÕES OU PROCEDURES

Utiliza-se parâmetros ou argumentos para passar valores para a função. Esses valores serão acessíveis dentro da função.

"""

def calculo_imc(altura: float, peso: float) -> float:
    return peso / (altura * altura)

if __name__ == "__main__":

    # Parâmentros passados de forma posicional, ou seja, precisa seguir a ordem dos parâmetros
    print(f"{calculo_imc(1.88, 92.3):.1f}")

    # Porém é possível passar os valores indicando quais parâmetros irão recebê-los.
    print(f"{calculo_imc(peso=87.5, altura=1.79):.1f}")

    # Existe um recurso chamado desempacotamento de valores onde se utiliza uma sixtaxe especial
    # para passar valores de uma sequência diretamente nos parâmetros de uma função.

    altura_peso_alberto = (1.81, 101.2)

    # Forma 01
    print(calculo_imc(altura_peso_alberto[0], altura_peso_alberto[1]))

    # Forma 02
    print(calculo_imc(*altura_peso_alberto))

    # Também podemos desempacotar os valores de um dicionário, dessa maneira estamos passando  os valores
    # para a função utilizando os nomes dos parâmetros.
    altura_peso_alberto = {"altura": 1.74, "peso": 107.3}
    print(f"{calculo_imc(**altura_peso_alberto):.1f}")