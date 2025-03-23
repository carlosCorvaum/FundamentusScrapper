import pandas as pd


def table_to_json(table):
    """
    Converte uma tabela HTML em um dicionário JSON.

    Args:
        table (BeautifulSoup): Tabela HTML parseada.

    Returns:
        dict: Dicionário JSON com pares chave-valor.
    """
    json_result = {}
    rows = table.find_all("tr")

    for row in rows:
        cells = row.find_all("td")
        for index_cell in range(0, len(cells), 2):
            key = cells[index_cell].get_text(strip=True)
            value = (
                cells[index_cell + 1].get_text(strip=True)
                if (index_cell + 1) < len(cells)
                else ""
            )
            original_key = key
            count = 1
            while key in json_result:
                key = f"{original_key}_{count}"
                count += 1
            json_result[key] = value

    print(json_result)
    return json_result


def clean_column_names(df):
    """
    Limpa os nomes das colunas removendo caracteres indesejados.

    Args:
        df (pd.DataFrame): DataFrame a ser limpo.
    """
    df.columns = [col.replace("?", "").replace("_0", "") for col in df.columns]


def filter_dataframe(df):
    """
    Filtra o DataFrame para incluir apenas colunas especificadas.

    Args:
        df (pd.DataFrame): DataFrame a ser filtrado.

    Returns:
        pd.DataFrame: DataFrame filtrado.
    """
    columns_to_keep = [
        "Dia",
        "Mês",
        "30 dias",
        "12 meses",
        "2024",
        "2023",
        "2022",
        "2021",
        "2020",
        "2019",
    ]
    available_columns = [col for col in columns_to_keep if col in df.columns]
    return df[available_columns]


def remove_columns_from_df(df, columns_to_remove):
    """
    Remove colunas específicas de um DataFrame.

    Args:
        df (pd.DataFrame): DataFrame a ser modificado.
        columns_to_remove (list of str): Colunas a serem removidas.

    Returns:
        pd.DataFrame: DataFrame com as colunas removidas.
    """
    return df.drop(columns=columns_to_remove, errors="ignore")


def add_papel_column(dataframes, papel):
    """
    Adiciona a coluna 'Papel' com o nome do papel como a primeira coluna nos DataFrames 1, 2, 3, 4 e 5.

    Args:
        dataframes (list): Lista de DataFrames a serem modificados.
        papel (str): Nome do papel a ser adicionado.

    Returns:
        list: Lista de DataFrames com a coluna 'Papel' adicionada.
    """
    for i in range(1, 6):
        if i < len(dataframes):
            dataframes[i]["Papel"] = papel
            cols = dataframes[i].columns.tolist()
            cols = ["Papel"] + [col for col in cols if col != "Papel"]
            dataframes[i] = dataframes[i][cols]
    return dataframes


def manager(tables, papel):
    """
    Função de transformação que converte tabelas em DataFrames, limpa e renomeia colunas.

    Args:
        tables (list): Lista de tabelas extraídas.
        papel (str): Nome do papel a ser adicionado nos DataFrames.

    Returns:
        list: Lista de DataFrames transformados.
    """
    # converter json_to_df
    dataframes = json_to_df(tables, papel)

    # Retirar o '?'
    for df in dataframes:
        df.columns = [col.replace("?", "").replace("_0", "") for col in df.columns]

    # renomenado campos do df 4
    rename_mapping = {
        "Receita Líquida": "Receita Líquida 12 meses",
        "Receita Líquida_1": "Receita Líquida 3 meses",
        "EBIT": "EBIT 12 meses",
        "EBIT_1": "EBIT 3 meses",
        "Lucro Líquido": "Lucro Líquido 12 meses",
        "Lucro Líquido_1": "Lucro Líquido 3 meses",
    }
    dataframes[4].rename(columns=rename_mapping, inplace=True)

    # Criando DF 5
    filtered_df = filter_dataframe(dataframes[2])
    columns_to_remove = filtered_df.columns.tolist()
    dataframes[2] = remove_columns_from_df(dataframes[2], columns_to_remove)
    dataframes.append(filtered_df)

    # Adicionando a primeira coluna papel PK em todos df
    dataframes = add_papel_column(dataframes, papel)

    # Dropando colunas residuais
    dataframes[2] = dataframes[2].drop(columns=["Oscilações", ""], errors="ignore")
    dataframes[3] = dataframes[3].drop(
        columns="Dados Balanço Patrimonial", errors="ignore"
    )
    dataframes[4] = dataframes[4].drop(
        columns=["Dados demonstrativos de resultados", "Últimos 12 meses"],
        errors="ignore",
    )

    return dataframes


def json_to_df(tables, papel):
    all_tables_json = [table_to_json(table) for table in tables]
    dataframes = [pd.DataFrame([table_json]) for table_json in all_tables_json]
    return dataframes
