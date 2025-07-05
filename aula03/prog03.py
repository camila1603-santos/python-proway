"""
FUNÇÕES OU PROCEDURES

É possível criar funções que possuam parâmetros opcionais, ou seja, parâmetros que não precisam receber um valor.
Para isso, é definido um valor padrão para esse parâmetro.

"""

def calculo_hora_extra(valor_hora: float, qtde_horas_extras: int = 0) -> float:
    return valor_hora * qtde_horas_extras

if __name__ == "__main__":

    print("{:.2f}".format(calculo_hora_extra(56, 3)))
    print("{:.2f}".format(calculo_hora_extra(qtde_horas_extras=1, valor_hora=60)))
    print("{:.2f}".format(calculo_hora_extra(valor_hora=20)))