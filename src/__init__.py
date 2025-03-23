from src.services.load import process_host
import json
import requests
from sqlalchemy import create_engine


def main():
    """
    Função principal para processar todos os papéis em paralelo.
    """
    with open("gold_stock_list.json", "r") as file:
        lista_papeis = json.load(file)

    session = requests.Session()
    engine = create_engine("postgresql+psycopg2://user:postgres@postgres/postgres")

    for papel in lista_papeis:
        # Gerencia as threads para processar papéis em paralelo
        info_stocks = process_host(papel, session, engine)
        if info_stocks != None:
            for i, df in enumerate(info_stocks):
                print(f"# DataFrame: {i}")
                print(df.T.to_string())
                print("\n" + "=" * 40 + "\n")

    session.close()
