# Extração
import requests


def fetch_html(url,session):
    """
    Faz a requisição HTTP para obter o conteúdo HTML da página.

    Args:
        url (str): URL da página.

    Returns:
        str: Conteúdo HTML ou None se falhar.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = session.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None
