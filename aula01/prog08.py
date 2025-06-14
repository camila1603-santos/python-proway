"""
Operadores em Python

OPERADORES LÓGICOS
São utilizados em conjunto com operadores de comparação em expressões. Podemos combinar várias comparações em um único valor final. Retornam sempre um booleano.
Operadores: and, or e not

"""

if __name__ == "__main__":

    #Operador and - retorna true caso os dois lados da expressão sejam true, senão retorna false
    print(5 > 4 and 3 > 1)
    print(5 > 4 and 3 < 1)
    print(5 < 4 and 3 > 1)
    print(5 < 4 and 3 < 1)
    print("----------------------")

    #Operador or - retorna true caso um dos lados seja true. Somente se ambos os lados forem false, então retorna false
    print(5 > 4 or 3 > 1)
    print(5 > 4 or 3 < 1)
    print(5 < 4 or 3 > 1)
    print(5 < 4 or 3 < 1)
    print("----------------------")

    #Operador not - nega o valor comparado, ou seja, se for true retornar false e se for false retorna true
    print(not 5 > 4)
    print(not 3 < 1)