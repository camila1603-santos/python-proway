"""
FUNÇÕES OU PROCEDURES

São blocos de códigos que executam uma determinada tarefa. Devido a sua natureza, funções são definidas
uma vez e utilizadas em diversas partes do código. Além disso, as funções podem receber valores através
de parâmetros e também podem retornar valores resultantes das tarefas realizadas. A utilização de funções
facilita o reuso de código.

Utiliza-se a palavra reservada "def" para criar funções. A função precisa retornar algo. 

"""

#Utilizamos o módulo datetime quando queremos trabalhar com data/hora

from datetime import datetime

def detalhe_data_hora_agora():
    print(datetime.now().strftime(
        "%H:%M %d/%m/%Y"
    ))


if __name__ == "__main__":
    detalhe_data_hora_agora()