import streamlit as st
import requests
from utils import scrape_movie_elements
from utils_html import generate_html_movie_card

imdb_home_url = "https://www.imdb.com/"

st.title("Movie Retriever")
st.write("Enter a movie description to find similar movies.")

# Input box for query
query = st.text_input("Movie description query:")

if st.button("Search"):
    if query:
        try:
            response = requests.post("http://127.0.0.1:8000/search", json={"query": query})
            response.raise_for_status()  # raise an exception for HTTP errors
            data = response.json()
            results = data.get("results", [])
            
            if results:
                st.write("### Results")
                # Iterate over each result and create a nicely styled box.
                for i, result in enumerate(results):
                    movie_elements = {}
                    movie_elements['title'] = result.get("title", "Unknown")
                    movie_elements['description'] = result.get("plot", "No description provided.")
                    movie_elements['score'] = result.get("sim_score", 0)
                    movie_elements['id'] = result.get("id", "Unknown")
                    movie_elements['imdb_url'] = imdb_home_url + f"title/{movie_elements['id']}"
                    movie_elements['poster_url'] = scrape_movie_elements([movie_elements['id']], element_keys=["full-size cover url"])[movie_elements['id']]["full-size cover url"]
                    
                    # Create an HTML card for each result
                    card_html = generate_html_movie_card(movie_elements)
                    st.markdown(card_html, unsafe_allow_html=True)
            else:
                st.info("No results found.")
        except requests.RequestException as e:
            st.error(f"Error retrieving results: {e}")
    else:
        st.error("Please enter a query before searching.")