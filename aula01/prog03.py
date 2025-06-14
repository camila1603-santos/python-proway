"""
Tipos de dados em Python - data type

TIPOS NUMÉRICOS

Em Python, temos três tipos númericos:

1. int = para números inteiros
2. float = para números com casas decimais
3. complex = para números complexos (imaginários)

"""

if __name__ == "__main__":

    base = 10

    numero = int(input("Informe um número: "))
    resultado = numero * base
    print(f"Número vezes a base: {resultado}.")

    # Mesmo se o resultado da divisão for um número inteiro, será gerado um número com casa
    # decimal (float)
    # As vezes o resultado retornado possui muitas casas decimais, porém podemos arredondar esse valor.
    # Estamos limitando a quantidade de casas deciamais a apenas uma
    novo_numero = resultado / 3
    print(f"{novo_numero:.1f}")

# Números complexos possuem uma parte real e uma parte imaginária

    numero_complexo = 45j

    print(numero_complexo)