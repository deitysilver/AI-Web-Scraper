import google.generativeai as genai
import streamlit
import requests
from bs4 import BeautifulSoup

genai.configure(api_key="API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

def generate(data):
    return model.generate_content(data).text

def scrape(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup.get_text()

streamlit.title("Web Scraper")
site_url = streamlit.text_input("Enter Website URL: ")

if site_url:
    streamlit.divider()
    if not site_url.startswith(("http://", "https://")):
        site_url = "http://" + site_url

    try:
        streamlit.subheader("Site Description")
        site_content = scrape(site_url)
        
        expander = streamlit.expander("Scraped Content:")
        expander.write(site_content)

        prompt = streamlit.text_input("Enter Prompt: ")

        if streamlit.button("Ask Anything"):
            streamlit.divider()
            response = generate("/n This is the data: /n" + site_content + "/n And this is the prompt" + prompt)
            streamlit.write(response)

    except Exception as e:
        streamlit.error(f"Error fetching the URL: {e}")
