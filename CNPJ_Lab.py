import requests
from bs4 import BeautifulSoup
import json
import time
# Função para obter os dados de uma ação
def get_stock_data(stock_code):
    # URL alvo
    url = f"https://www.dadosdemercado.com.br/acoes/{stock_code}"

    # Realizando a requisição GET
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Parser
        soup = BeautifulSoup(response.content, 'lxml')
        data = {}
        about_params = soup.find("div", class_="about-params")

        if about_params:
            try:
                # Razão Social
                razao_social = about_params.find("span", text="Razão social").find_next("span").get_text(strip=True)
                data["razao_social"] = razao_social

                # CNPJ
                cnpj = about_params.find("span", text="CNPJ").find_next("span").get_text(strip=True)
                data["cnpj"] = cnpj

                # Classificação Setorial
                classificacao_setorial = about_params.find("span", text="Classificação setorial B3").find_next("span").get_text(strip=True)
                data["classificacao_setorial"] = classificacao_setorial

            except AttributeError:
                print(f"Não foi possível encontrar um ou mais elementos na página para {stock_code}.")
        else:
            print(f"A estrutura esperada não foi encontrada na página para {stock_code}.")
        
        return data
    else:
        print(f"Falha ao acessar a página para {stock_code}. Status code: {response.status_code}")
        return None

# Lista de ações
stocks = ["vale3", "CLSA3", "petr3"]

# Obtendo dados para cada ação
results = []
for stock in stocks:
    print(f"Processando {stock}...")
    stock_data = get_stock_data(stock)
    if stock_data:
        stock_data["codigo"] = stock  # Adicionando o código da ação nos dados
        results.append(stock_data)
    time.sleep(5)
    

# Convertendo para JSON e exibindo
json_results = json.dumps(results, indent=4, ensure_ascii=False)
print(json_results)

