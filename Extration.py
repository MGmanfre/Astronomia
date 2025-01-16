import requests
import pandas as pd
import mysql.connector
import os
from io import StringIO
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from time import sleep

# Carregar as variáveis do arquivo .env
load_dotenv()

# URLs das APIs
EXOPLANET_API_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

# Chave de API
api_key = os.getenv("EXOPLANET_API_KEY")

# Função para conectar ao banco de dados
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("DB_PASSWORD"),
            database="db_astronomy"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

# Função para limpar e formatar os dados
def clean_data(data):
    # Substituir NaN por None (compatível com MySQL)
    return data.replace({pd.NA: None, float('nan'): None, None: None})

# Função genérica para processar tabelas HTML usando BeautifulSoup
def extract_tables_with_bs4(html_text):
    try:
        soup = BeautifulSoup(html_text, "html.parser")
        tables = soup.find_all("table")
        dataframes = [pd.read_html(str(table))[0] for table in tables]
        return dataframes[0] if dataframes else pd.DataFrame()
    except Exception as e:
        print(f"Erro ao processar HTML com BeautifulSoup: {e}")
        return pd.DataFrame()

# Coleta de dados de exoplanetas
def get_exoplanets():
    params = {
        "query": """
            SELECT pl_name, pl_bmasse, pl_rade, pl_orbper, sy_dist
            FROM ps
            WHERE pl_bmasse IS NOT NULL AND pl_rade IS NOT NULL AND sy_dist IS NOT NULL
        """,
        "format": "json",
        "api_key": api_key
    }
    response = requests.get(EXOPLANET_API_URL, params=params)
    if response.status_code == 200:
        try:
            return pd.DataFrame(response.json())
        except ValueError:
            print(f"Erro ao decodificar os dados de exoplanetas: {response.text}")
            return pd.DataFrame()
    else:
        print(f"Erro ao buscar exoplanetas: {response.status_code}")
        return pd.DataFrame()


# Inserção de exoplanetas no banco de dados
def insert_exoplanets(data):
    connection = connect_to_db()  # Função para conectar ao banco
    if connection:
        cursor = connection.cursor()
        query = """
        INSERT INTO Exoplanetas (Nome, Massa, Raio, Periodo_Orbital, Distancia)
        VALUES (%s, %s, %s, %s, %s)
        """
        # Limpar os dados antes da inserção
        data = clean_data(data)
        for _, row in data.iterrows():
            try:
                cursor.execute(query, (
                    row['pl_name'],   # Nome do exoplaneta
                    row['pl_bmasse'], # Massa em massas terrestres
                    row['pl_rade'],   # Raio em raios terrestres
                    row['pl_orbper'], # Período orbital
                    row['sy_dist']    # Distância em parsecs
                ))
            except mysql.connector.Error as err:
                print(f"Erro ao inserir exoplaneta {row['pl_name']}: {err}")
        connection.commit()
        cursor.close()
        connection.close()
        print(f"{len(data)} exoplanetas inseridos no banco de dados.")

# Função principal
def main():
    print("Buscando exoplanetas...")
    exoplanets = get_exoplanets()
    if not exoplanets.empty:
        insert_exoplanets(exoplanets)

# Código de execução principal
if __name__ == "__main__":
    main()
