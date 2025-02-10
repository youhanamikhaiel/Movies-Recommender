from typing import List, Dict, Optional
import ast
import requests
import pandas as pd
from imdb import IMDb
from bs4 import BeautifulSoup

ia = IMDb()


# Function to scrape movie description
def get_movie_description(movie_id: str) -> Optional[str]:
    """
    DO NOT USE
    Scrape movie description from IMDb website only non-dynamic content
    """
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

def scrape_movie_elements(movie_ids: List[str], element_keys: List = None) -> Dict[str, str]:
    all_elements = {}
    for movie_id in movie_ids:
        all_elements[movie_id] = {}
        movie = ia.get_movie(movie_id[2:])
        for key in element_keys:
            all_elements[movie_id][key] = movie[key]
    return all_elements

# convert lists in columns to strings
def process_list_columns(data_df: pd.DataFrame, columns_names: List[str]) -> pd.DataFrame:
    """
    Convert stringified lists to actual lists in a dataframe
    """
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


def get_movie_metadata(imdb_id: str, retrieved_keys: List[str]) -> Dict:
    movie = ia.get_movie(imdb_id)
    movie_dict = {}
    cast_and_crew = []
    cast_and_crew_in_movies = []
    for key in retrieved_keys:
        if key in ["cast", "director", "writer"]:
            for person in movie[key]:
                if person:
                    person_name = person['name']
                    person_id = person.personID
                    new_dict = {'personID': person_id, 'name': person_name, 'category': key}
                    if new_dict not in cast_and_crew:
                        cast_and_crew.append({'personID': person_id, 'name': person_name, 'category': key})
                    if key not in movie_dict:
                        movie_dict[key] = []
                    movie_dict[key].append(person.personID)
                    cast_and_crew_in_movies.append({'movie_id': imdb_id,
                                                    'person_id': person_id, 
                                                    'category': key, 
                                                    'role': person.currentRole['name'] if key == "cast" else ""})
        else:
            movie_dict[key] = movie[key]

    return movie_dict, cast_and_crew, cast_and_crew_in_movies
