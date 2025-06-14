"""
Laços de condição em Python

match case

Utilizado nos casos onde temos mais controle dos resultados possíveis de uma comparação.

"""

if __name__ == "__main__":

    comando = input("Informe o comando que deseja executar: ").upper()

    match comando:
        case "INICIAR":
            print("O processo foi iniciado.")
        
        case "INTERROMPER":
            print("O processo foi interrompido.")

        case "FINALIZAR":
            print("O processo foi finalizado.")
        
        case _:
            print(f"Comando '{comando}' desconhecido")