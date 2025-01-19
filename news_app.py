import  streamlit as st
import requests

def fetch_articles(api_key, category, language, page_size=10):
    """
    Fetch top headlines from NewsAPI using the provided category and language.
    Returns JSON response if successful, or None if an error occurs.
    """
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": category,
        "language": language,
        "apiKey": api_key,
        "pageSize": page_size
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching articles: {e}")
        return None

def main():
    st.title("News Aggregator")
    st.markdown(
        """
        This Streamlit app uses [NewsAPI.org](https://newsapi.org/) to fetch the latest headlines
        from various topics and languages. 
        """
    )

    # Sidebar for inputs
    st.sidebar.title("Configuration")
    
    # Check if the API key is in st.secrets
    if "NEWS_API_KEY" in st.secrets:
        api_key = st.secrets["NEWS_API_KEY"]
    else:
        api_key = st.sidebar.text_input("Enter your News API Key:", type="password")
    
    # Select the category
    category = st.sidebar.selectbox(
        "Choose a topic:",
        [
            "business",
            "entertainment",
            "general",
            "health",
            "science",
            "sports",
            "technology"
        ],
        index=2  # "general" by default
    )
    
    # Select the language
    language = st.sidebar.selectbox(
        "Choose a language:",
        [
            "ar",  # Arabic
            "de",  # German
            "en",  # English
            "es",  # Spanish
            "fr",  # French
            "it",  # Italian
            "nl",  # Dutch
            "no",  # Norwegian
            "pt",  # Portuguese
            "ru",  # Russian
            "se",  # Northern Sami
            "ud",  # Urdu
            "zh"   # Chinese
        ],
        index=2  # "en" by default
    )
    
    # Number of articles to display
    page_size = st.sidebar.slider("Number of articles to display:", 1, 50, 10)
    
    if api_key:
        # Fetch the articles
        data = fetch_articles(api_key, category, language, page_size)
        
        if data and data.get("status") == "ok":
            articles = data.get("articles", [])
            
            if articles:
                st.success(f"Found {len(articles)} articles about **{category}** in **{language}**")
                for idx, article in enumerate(articles, start=1):
                    st.subheader(f"{idx}. {article.get('title')}")
                    st.write(f"**Source:** {article['source'].get('name')}")
                    st.write(f"**Author:** {article.get('author', 'N/A')}")
                    st.write(f"**Published At:** {article.get('publishedAt', 'N/A')}")
                    st.write(article.get("description", "No description available."))
                    if article.get("url"):
                        st.markdown(f"[Read more...]({article['url']})")
                    st.write("---")
            else:
                st.warning("No articles found for the selected options.")
        else:
            st.warning("Could not retrieve articles. Please check your API key or settings.")
    else:
        st.warning("Please enter your News API Key in the sidebar.")

if __name__ == "__main__":
    main()