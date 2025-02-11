import streamlit as st
import requests

def get_nyt_top_stories(api_key, section="home"):
    """Fetch NYT top stories for a given section."""
    url = f"https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from NYT API. Please check your API key or try again later.")
        return None

def main():
    st.title("NYT Top Stories")


    if "NYT_API_KEY" in st.secrets:
        api_key = st.secrets["NYT_API_KEY"]
    else:
        api_key = st.text_input("Enter your NYT API key:", type="password")
    
    section = st.selectbox("Select a Section", 
                                   ["home", "science", "arts", "us", "world", "technology"])
    
    if api_key:
        data = get_nyt_top_stories(api_key, section)
        if data:
            # st.subheader(f"Top Stories in the {section.capitalize()} Section")
            for article in data.get("results", []):
                title = article.get("title", "No title")
                abstract = article.get("abstract", "")
                byline = article.get("byline", "")
                url = article.get("url", "")
                published_date = article.get("published_date", "")
                
                # Display article title as a clickable header
                st.markdown(f"### [{title}]({url})")
                
                # Display the first image from multimedia, if available
                multimedia = article.get("multimedia")
                if multimedia:
                    image_url = multimedia[0].get("url")
                    caption = multimedia[0].get("caption", "")
                    if image_url:
                        st.image(image_url, caption=caption, use_container_width=True)
                
                st.write(abstract)
                st.write(f"**By:** {byline} | **Published:** {published_date}")
                st.markdown("---")
    else:
        st.info("Please enter your NYT API key in the sidebar.")

if __name__ == '__main__':
    main()
