import os
import pickle
import time
import pandas as pd
from sqlalchemy import create_engine, text


def retorna_dados():
    # Define cache file path
    CACHE_FILE = "cached_data.pkl"

    # SQL Query
    DATA_QUERY = text("""
    SELECT grupo, codigo_ativo, data_referencia, data_vencimento, duration, indexador, taxa_emissao, taxa_indicativa, emissor
    FROM dados_debenture;
    """)

    def is_cache_expired(expiry_time=6*60*60):  # Expiry in seconds
        """Check if cache file is expired."""
        if not os.path.exists(CACHE_FILE):
            return True  # Cache doesn't exist, force a fetch

        last_modified = os.path.getmtime(CACHE_FILE)  # Get last modified time
        return (time.time() - last_modified) > expiry_time  # Check expiration

    def get_cached_data():
        """Check if cached data exists and return it if valid."""
        if os.path.exists(CACHE_FILE) and not is_cache_expired():
            # print("✅ Using cached data. No database connection needed.")
            with open(CACHE_FILE, "rb") as f:
                return pickle.load(f)

        return None  # Return None if cache is expired or doesn't exist

    def fetch_data_from_db():
        """Connect to the database and fetch data if cache is expired or not available."""
        # print("⚡ Fetching data from the database...")
        engine = create_engine(
            "postgresql://postgres:admin@192.168.88.61:5432/yield_debentures")

        with engine.connect() as conexao:
            resultado = conexao.execute(DATA_QUERY)
            dados = resultado.fetchall()

        df = pd.DataFrame(dados, columns=resultado.keys())

        # Store the fetched data in cache
        with open(CACHE_FILE, "wb") as f:
            pickle.dump(df, f)

        return df

    # ✅ Ensure data is only fetched if necessary
    df = get_cached_data()

    if df is None:  # If cache is expired or unavailable, fetch from DB
        df = fetch_data_from_db()

    # Print the first few rows
    # print(df.head())
    return df
