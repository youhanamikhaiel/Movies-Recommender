import ast
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import pandas as pd
from imdb import IMDb
import yaml


# Function to scrape movie description
def get_movie_description(movie_id: str) -> Optional[str]:
    url = f'https://www.imdb.com/title/{movie_id}/'
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract the movie description
        description = soup.find('span', {'data-testid': 'plot-xl'}).get_text(strip=True)
        return description
    except Exception as e:
        print(f"Error fetching description for {movie_id}: {e}")
        return None


# convert lists in columns to strings
def process_list_columns(data_df: pd.DataFrame, columns_names: List[str]) -> pd.DataFrame:
    for column_name in columns_names:
        if column_name not in data_df.columns:
            print(f'Column {column_name} not found in dataframe')
            continue

        if data_df[column_name].dtype != 'object':
            print(f'Column {column_name} is not of type object')
            continue

        # Convert stringified lists to actual lists
        data_df[column_name] = data_df[column_name].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])

    return data_df

def scrape_movie_elements(movie_ids: List[str], element_keys: List = None) -> Dict[str, str]:
    """
    TODO: This function need to change to instead get information from the database, and if
          not found it uses the API
    """
    ia = IMDb()
    all_elements = {}
    for movie_id in movie_ids:
        all_elements[movie_id] = {}
        movie = ia.get_movie(movie_id[2:])
        for key in element_keys:
            all_elements[movie_id][key] = movie[key]

    return all_elements


def load_config(file_path="config/config.yaml"):
    with open(file_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config
