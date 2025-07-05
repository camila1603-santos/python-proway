"""
ESTRUTURAS DE REPETIÇÃO EM PYTHON

Laço for

Utilizado quando queremos iterar sobre um objeto, ou seja, acessar de maneira sequencial os itens
desse objeto. Geralmente é utilizado com listas e tuplas, sendo a condição de interrupção desse laço,
o fim dos itens a serem lidos.

"""

if __name__ == "__main__":

    """
    Abaixo criada lista que é uma estrutura de dados que armazena outros tipos de dados,
    inclusive outras listas. Listas são indexáveis, ordenadas, iteráveis e mutáveis.

    Duas formas de criar listas:
    1) utilizando colchetes ["item1", "item2", "etc"]
    2) utilizando a função built-in list -> list("item1", "item2", "etc")
    """

    lista_compras = ["Banana", "Carne de Frango", "Ovos", "Rollmops", "Manteiga"]

    for item in lista_compras:
        print(item)


# Dentro do laço for é possível utilizar comandos. Exemplos:
# Comando break: interrompe imediatamente a execução do loop, independente de quantos itens faltam para ser lidos.

for item in lista_compras:
    if item == "Rollmops":
        print("Credo! Joga fora!")
        break # ainda teria o item manteiga, porém foi interrompido
    print(item)

# Comando continue: interrompe a iteração atual, independentemente de existirem mais instruções a serem executadas no bloco.
# Ou seja, ele volta para o início do loop para ler o próximo item. 

for item in lista_compras:
    if item == "Rollmops":
        print("Nem todo mundo gosta de rollmops, indo para o próximo item.")
        continue # ele imprime o texto "Nem todo mundo gosta de rollmops, indo para o próximo item." e volta para o
                 # próximo item da lista, no caso, manteiga
    print(item)


# Junto com o laço for é possível utilizar funções específicas como range() e enumerate().

print("####### Função range() #############")

for item in range(10):
    print(item)

# Função enumerate retorna um par de valores: sendo o primeiro o índice e o segundo o item do objeto sendo iterado.
# Serve apenas para formatar essa saída

print("####### enumerate() #############")
for index, item in enumerate(lista_compras, start=1):
    print(f"{index}) {item}")


""" 
Nas listas indexáveis é possível acessar os valores informando uma posição que chamamos de índice.

lista = ["Python", "Java", "PHP", "SQL", "JavaScript"]
            0        1       2      3          4 
           -5       -4      -3     -2         -1 
Além disso, podemos utilizar índices negativos, com o último item da lista sempre começando com -1.
Se tiver uma lista muito grande, utilizar para saber o último item da lista colocando o parâmetro -1

"""

print("####### listas indexáveis #############")

#Acessando o 4 item da lista
print(lista_compras[3]) # posição na lista menos 1

#Acessando o último item da lista
print(lista_compras[-1])

print("####### métodos #############")

# Listas são objetos e é possível utilizar métodos para serem utilizados nessa lista

# append insere um item no final da lista
lista_compras.append("Cebola")
lista_compras.append("Tomate")
# insert insere um item na lista na posição informada
lista_compras.insert(3, "Queijo")
# extend insere os itens de um iterável (listas, tuplas, etc) no final da lista atual
lista_compras.extend(("Iogurte", "Leite",))

# Como listas são mutáveis, podemos alterar um valor indicando uma posição. Exemplo: substituir o valor rollmops por pimenta.
lista_compras[4] = "Pimenta"

print(lista_compras)

# Slicing: extrai uma parte da lista, utilizando os índices
print("####### slicing #############")

#print(lista_compras[3:7]) #coloca o item limite, no caso o item 7, não entra. Inclui o primeiro índice e exclui o último
# Se não colocar nada [3:] ou [:7] pega até ou a partir.
# Se colocar [::-1] gera lista invertida


print("####### CÓPIA DE LISTAS #############")

# Se não utilizar o método copy, não vai copiar a lista corretamente, quando realizar as exclusões, vai alterar
# também a lista_compras. Pode utilizar o slice também, ficaria:
# lista_laticinios = lista_compras[::]
lista_laticinios = lista_compras.copy()
# O método pop() recebe o índice do item que será removido da lista e retorna o valor removido. Se não passar nada, remove7
# o último item.
lista_laticinios.pop(0)
lista_laticinios.pop(0)
lista_laticinios.pop(0)

lista_laticinios.remove("Pimenta")
lista_laticinios.remove("Cebola")
lista_laticinios.remove("Tomate")

print(lista_laticinios)

