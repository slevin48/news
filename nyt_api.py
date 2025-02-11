import requests, json
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("NYT_API_KEY")
# days = 7  # Options: 1, 7, or 30
# url = f"https://api.nytimes.com/svc/mostpopular/v2/mostviewed/all-sections/{days}.json?api-key={api_key}"

# response = requests.get(url)
# data = response.json()
# print(data)

section = "technology"  # try "home", "science", "arts", "us", "world" or "technology".
url = f"https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={api_key}"

response = requests.get(url)
data = response.json()
print(data)
with open('nyt.json', 'w') as f:
    json.dump(data, f, indent=4)
