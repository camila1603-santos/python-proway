import pymysql
import pymysql.cursors
import requests
import os

from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":

    connection = pymysql.connect(
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST"), #corresponde a máquina local
        port=int(os.getenv("DATABASE_PORT")),
        database=os.getenv("DATABASE_NAME")
    )

    cursor = connection.cursor()

    comand = """
        CREATE TABLE IF NOT EXISTS tb_cryptos(
            id INT PRIMARY KEY AUTO_INCREMENT,
            simbolo VARCHAR(10) NOT NULL,
            nome VARCHAR(20) NOT NULL,
            preco_usd DOUBLE NOT NULL,
            market_cap_usd DOUBLE NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
"""

    cursor.execute(comand)

    #URL DA API

    url = "https://api.coinlore.net/api"

    crypto_id = input("Informe o código da moeda: ")
    response = requests.get(
        f"{url}/ticker?id={crypto_id}"
    )

    ticker_info = response.json()[0]

    command = """
        INSERT INTO tb_cryptos(simbolo, nome, preco_usd, market_cap_usd)
        VALUES
        (%s, %s, %s, %s)"""
    
    cursor.execute(
        command,
        (
            ticker_info.get("symbol"),
            ticker_info.get("name"),
            ticker_info.get("price_usd"),
            ticker_info.get("market_cap_usd"),
        )
    )

    connection.commit()

    print(ticker_info)