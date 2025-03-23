from src.services.extract import extract
from src.services.transform import manager
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine


def process_host(papel, session, engine):
    """
    Processa dados para um único papel, realizando as etapas de extração, transformação e carga.

    Args:
        papel (str): Código do papel.

    Returns:
        list: Lista de DataFrames transformados e carregados.
    """
    tables = list(extract(papel))
    if manager(tables, papel) != None:
        tables = manager(tables, papel)
        db_persistance(tables, engine)
        return tables
    return None


def db_persistance(tables, engine):
    # Definir os nomes das tabelas para os DataFrames
    tables_names = [
        "stock_info",  # DataFrame 0
        "market_value",  # DataFrame 1
        "valuation_metrics",  # DataFrame 2
        "balance_sheet",  # DataFrame 3
        "income_statement",  # DataFrame 4
        "stock_performance",  # DataFrame 5
    ]

    for df, table_name in zip(tables, tables_names):
        try:
            engine = create_engine(
                "postgresql+psycopg2://postgres:postgres@localhost/postgres"
            )
            df.to_sql(name=table_name, con=engine, if_exists="append")
        except SQLAlchemyError as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
