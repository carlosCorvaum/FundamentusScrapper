from bs4 import BeautifulSoup
from src.utils.http_request import fetch_html
import requests
import json


def parse_html(html_content):
    """
    Faz o parse do HTML e extrai todas as tabelas.

    Args:
        html_content (str): Conteúdo HTML da página.

    Returns:
        list: Lista de tabelas encontradas.
    """
    try:
        soup = BeautifulSoup(html_content, "lxml")
        return soup.find_all("table")
    except Exception as e:
        print(f"Erro ao parsear HTML: {e}")
        return []


def extract(papel):
    """
    Função de extração que obtém as tabelas da página HTML de um papel específico.

    Args:
        papel (str): Código do papel.

    Returns:
        list: Lista de tabelas extraídas.
    """
    url = f"https://www.fundamentus.com.br/detalhes.php?papel={papel}"

    session = requests.Session()
    html_content = fetch_html(url, session)
    session.close()

    if html_content:
        return parse_html(html_content)
    else:
        return []
