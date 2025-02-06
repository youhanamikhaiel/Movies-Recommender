from typing import Dict, Any



def generate_html_movie_card(movie: Dict[str, Any]) -> str:
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
                        <img src="{movie['poster_url']}" alt="{movie['title']} Poster" style="
                            width: 120px;
                            height: auto;
                            border-radius: 8px;
                            margin-right: 16px;
                        ">
                        <div style="flex: 1;">
                            <h3 style="margin-bottom: 8px;">
                                <a href="{movie['imdb_url']}" target="_blank" style="text-decoration: none; color: #007BFF;">
                                    {movie['title']}
                                </a>
                            </h3>
                            <p style="margin-bottom: 4px;"><strong>Description:</strong> {movie['description']}</p>
                            <p style="margin: 0;"><strong>Similarity Score:</strong> {movie['score']:.4f}</p>
                        </div>
                    </div>
                    """
    return card_html
