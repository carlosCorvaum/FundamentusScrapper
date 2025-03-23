import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import json
import os


def extract_table_from_page(url):
    """
    Extrai uma tabela HTML de uma página web e retorna como um DataFrame do Pandas.

    Parameters:
        url (str): URL da página web com a tabela.

    Returns:
        pd.DataFrame: Tabela extraída da página.

    Raises:
        ValueError: Se a tabela não for encontrada na página.
        RequestException: Para erros de rede.
    """
    try:
        # Envio da requisição HTTP
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Garante que uma exceção seja levantada para erros de HTTP

        # Parsing do HTML com BeautifulSoup e lxml
        soup = BeautifulSoup(response.content, "lxml")

        # Navegação até a tabela
        table = soup.select_one("div.center > div.conteudo.clearfix > table#resultado")
        if table:
            # Usando StringIO para envolver o HTML literal
            table_html = str(table)
            return pd.read_html(StringIO(table_html), flavor="lxml")[0]
        else:
            raise ValueError("Tabela não encontrada, verifique o caminho HTML.")
    except requests.RequestException as e:
        raise ValueError(f"Erro na requisição HTTP: {e}")
    except Exception as e:
        raise ValueError(f"Erro inesperado: {e}")


def save_papel_to_json(df, folder_name, file_name):
    """
    Salva os valores do campo 'Papel' do DataFrame em um arquivo JSON na pasta especificada.

    Parameters:
        df (pd.DataFrame): DataFrame contendo os dados.
        folder_name (str): Nome da pasta onde o arquivo JSON será salvo.
        file_name (str): Nome do arquivo JSON a ser criado.
    """
    # Cria a pasta se não existir
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    if "Papel" in df.columns:
        # Extrai a coluna 'Papel'
        papel_list = df["Papel"].tolist()
        # Salva em JSON na pasta especificada
        file_path = os.path.join(folder_name, file_name)
        with open(file_path, "w") as file:
            json.dump(papel_list, file, indent=4)
        print(
            f"Arquivo JSON '{file_name}' criado com sucesso na pasta '{folder_name}'."
        )
    else:
        raise ValueError("'Papel' não encontrado no DataFrame.")


# URL fornecida
url = "https://www.fundamentus.com.br/resultado.php/api/"
try:
    df = extract_table_from_page(url)
    # Nome da pasta e do arquivo JSON
    folder_name = "all_stocks"
    json_file_name = "all_stocks.json"
    save_papel_to_json(df, folder_name, json_file_name)
except Exception as e:
    print(f"Erro: {e}")
