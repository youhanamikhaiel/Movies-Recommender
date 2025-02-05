import streamlit as st
import requests
from utils import scrape_movie_elements

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
                    title = result.get("title", "Unknown")
                    description = result.get("plot", "No description provided.")
                    score = result.get("sim_score", 0)
                    id = result.get("id", "Unknown")
                    imdb_url = imdb_home_url + f"title/{id}"
                    poster_url = scrape_movie_elements([id], element_keys=["full-size cover url"])[id]["full-size cover url"]
                    
                    # Create an HTML card for each result
                    card_html = f"""
                                <div style="
                                    display: flex;
                                    align-items: center;
                                    border: 1px solid #ddd;
                                    border-radius: 8px;
                                    padding: 16px;
                                    margin-bottom: 16px;
                                    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
                                    background-color: #f9f9f9;
                                    max-width: 600px;
                                ">
                                    <img src="{poster_url}" alt="{title} Poster" style="
                                        width: 120px;
                                        height: auto;
                                        border-radius: 8px;
                                        margin-right: 16px;
                                    ">
                                    <div style="flex: 1;">
                                        <h3 style="margin-bottom: 8px;">
                                            <a href="{imdb_url}" target="_blank" style="text-decoration: none; color: #007BFF;">
                                                {title}
                                            </a>
                                        </h3>
                                        <p style="margin-bottom: 4px;"><strong>Description:</strong> {description}</p>
                                        <p style="margin: 0;"><strong>Similarity Score:</strong> {score:.4f}</p>
                                    </div>
                                </div>
                                """
                    st.markdown(card_html, unsafe_allow_html=True)
            else:
                st.info("No results found.")
        except requests.RequestException as e:
            st.error(f"Error retrieving results: {e}")
    else:
        st.error("Please enter a query before searching.")