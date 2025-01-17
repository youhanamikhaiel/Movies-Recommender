import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from tqdm import tqdm
import time
import ast
from typing import List, Dict, Optional
import pandas as pd


# Function to scrape movie description
def get_movie_description(movie_id: str) -> Optional[str]:
    url = f'https://www.imdb.com/title/{movie_id}/'
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' }
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract the movie description
        description = soup.find('span', {'data-testid': 'plot-xl'}).get_text(strip=True)
        return description
    except Exception as e:
        print(f"Error fetching description for {movie_id}: {e}")
        return None
    


# Function to scrape movie descriptions and update the dataframe
def scrape_movie_descriptions(movie_ids: List[str]) -> Dict[str, str]:
    descriptions = {}
    for movie_id in movie_ids:
        description = get_movie_description(movie_id)
        if description:
            descriptions[movie_id] = description
        time.sleep(0.05)
    return descriptions


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