# Colocar "if __name__ == "__main__":" é uma boa prática, mas não é obrigatório. É como se fosse o método main do Java ou C#.
# Todo arquivo py podemos chamar de módulo
# Função built in - automaticamente carregada dentro do Python. É diferente dos métodos da biblioteca padrão do Python.
if __name__ == "__main__":

    # Sempre que uma linha termina com dois pontos, como está acima, um novo bloco de código é criado. Indentação. 

    # A linha abaixo atribui o valor de retorno da função built-in input() a variável nome. 
    # No caso da função input, ela retorna o valor que foi digitado pelo terminal no formato string. Utilizamos o operador de atribuição = para salvar esse
    # valor variável nome. Como o Python é uma linguagem de tipagem dinâmica, o tipo dessa variável será definido automaticamente em tempo de execução
    # não sendo obrigatório indicarmos o tipo de variável, como estamos fazendo abaixo:
    nome: str = input("Informe o seu nome: ")

    # o "f" é utilizado para concatenar string
    print(f"Olá {nome}, bem-vindo(a) ao curso de Python.")