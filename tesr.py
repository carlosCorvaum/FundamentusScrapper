import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import unicodedata


def db_persistance(df):
    try:
        engine = create_engine(
            "postgresql+psycopg2://postgres:postgres@localhost/postgres"
        )
        df.to_sql(name="testa", con=engine, if_exists="append")
    except SQLAlchemyError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")


data = {
    "Papel": ["PETR3"],
    "Cotação": ["41,13"],
    "Tipo": ["ON"],
    "Data últ cot": ["06/09/2024"],
    "Empresa": ["PETROBRAS ON"],
    "Min 52 sem": ["30,58"],
    "Setor": ["Petróleo, Gás e Biocombustíveis"],
    "Max_52_sem": ["43,29"],
    "Subsetor": ["Exploração, Refino e Distribuição"],
    "Vol_$_méd (2m)": ["360.394.000"],
}
# Criando o DataFrame
df = pd.DataFrame(data)
print(df)


db_persistance(df)
