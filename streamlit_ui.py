import streamlit as st
import requests
from utils.utils_data import scrape_movie_elements
from utils.utils import load_config
from utils.utils_html import generate_html_movie_card
from src.chatbot.chatbot_metadata import system_message

config = load_config()

imdb_home_url = config["data"]["imdb_home_url"]
api_url = "http://" + config["api"]["host"] + ":" + str(config["api"]["port"])


# ---------------------- Chatbot Side Panel ----------------------

# Initialize chat panel state
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

# Toggle chat panel
if st.button("💬 Chat with us", key="chat_toggle"):
    st.session_state.chat_open = not st.session_state.chat_open

# Display chat panel
if st.session_state.chat_open:
    with st.sidebar:
        st.header("💬 Chat Support")

        if "messages" not in st.session_state:
            st.session_state.messages = system_message

        # Display chat history
        for message in st.session_state.messages[1:]:
            role, text = message
            st.chat_message(role).write(text)

        # Chat input
        user_input = st.chat_input("Type your message...")
        if user_input:
            # Append user message
            st.session_state.messages.append(("user", user_input))
            try:
                response = requests.post(api_url + config["api"]["chatbot_endpoint"],
                                         json={"message": st.session_state.messages},
                                         timeout=60)

                if response.status_code == 200:
                    bot_response = response.json().get("response", "No response received.")
                else:
                    bot_response = f"Error: {response.status_code}"

            except requests.exceptions.RequestException:
                bot_response = "Error: Unable to connect to chat server."

            # Append bot response to session state
            st.session_state.messages.append(("assistant", bot_response))

            # Force a rerun to display the new message
            st.rerun()

# ---------------------- Movie Retriever Main Panel ----------------------

st.title("Movie Retriever")
st.write("Enter a movie description to find similar movies.")

if "search_results" not in st.session_state:
    st.session_state.search_results = []

# Input box for query
query = st.text_input("Movie description query:")

if st.button("Search"):
    if query:
        try:
            response = requests.post(api_url + config["api"]["rag_endpoint"],
                                     json={"query": query},
                                     timeout=10)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            if results:
                st.session_state.search_results = []

            if results:
                for i, result in enumerate(results):
                    movie_elements = {}
                    movie_elements['title'] = result.get("title", "Unknown")
                    movie_elements['description'] = result.get("plot", "No description provided.")
                    movie_elements['score'] = result.get("sim_score", 0)
                    movie_elements['id'] = result.get("id", "Unknown")
                    movie_elements['imdb_url'] = imdb_home_url + f"title/{movie_elements['id']}"
                    movie_elements['poster_url'] = scrape_movie_elements([movie_elements['id']],
                                                                          element_keys=["full-size cover url"])[movie_elements['id']]["full-size cover url"]

                    # Caching movie results for faster access
                    st.session_state.search_results.append(movie_elements)
            else:
                st.info("No results found.")
        except requests.RequestException as e:
            st.error(f"Error retrieving results: {e}")
    else:
        st.error("Please enter a query before searching.")

if st.session_state.search_results:
    st.write("### Results")
    for movie in st.session_state.search_results:
        card_html = generate_html_movie_card(movie)
        st.markdown(card_html, unsafe_allow_html=True)
