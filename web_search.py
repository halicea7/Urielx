# web_search.py

import requests
import spacy
import pdfplumber
import time
from textblob import TextBlob
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel

# Load SpaCy NLP model
nlp = spacy.load("en_core_web_sm")


def get_search_results(query, num_results=10):
    """Fetch search results from DuckDuckGo while avoiding blocked sites."""
    blocked_sites = ["researchgate.net", "academia.edu", "sciencedirect.com"]
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=num_results)
            urls = [result["href"] for result in results if not any(site in result["href"] for site in blocked_sites)]
        return urls
    except Exception as e:
        print(f"❌ Error retrieving search results: {e}")
        return []


def extract_text_from_pdf(url):
    """Extracts text from a PDF URL."""
    try:
        print(f"📄 Downloading PDF: {url}")
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0'})

        response = session.get(url, timeout=20)
        response.raise_for_status()

        with open("temp.pdf", "wb") as file:
            file.write(response.content)

        with pdfplumber.open("temp.pdf") as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        
        return text if text else "No meaningful text found in PDF."
    except Exception as e:
        print(f"❌ Error extracting PDF content: {e}")
        return "Error retrieving PDF content."


def extract_text_from_url(url):
    """Extracts readable text from webpages."""
    if url.endswith(".pdf"):
        return extract_text_from_pdf(url)

    try:
        print(f"🌍 Scraping URL: {url}")
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        main_content = soup.find("article") or soup.find("div", class_="content") or soup.body
        paragraphs = main_content.find_all("p") if main_content else []

        text = " ".join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 30])
        return text if len(text) > 100 else "No meaningful text found."

    except Exception as e:
        print(f"❌ Error extracting from {url}: {e}")
        return "Error retrieving content."


def search_and_extract(topic, num_results=5):
    """Performs a search and extracts meaningful text from the results."""
    urls = get_search_results(topic, num_results)
    extracted_data = []

    for url in urls:
        text = extract_text_from_url(url)
        if "Error" in text or "No meaningful text" in text:
            continue
        extracted_data.append({"url": url, "text": text})

    return extracted_data


class WebSearchTool(BaseTool):
    """CrewAI-compatible tool for web search and information extraction."""
    
    name = "Web Search"
    description = "Searches the web for relevant information and extracts meaningful content."
    
    def _run(self, query: str) -> str:
        """Runs a web search and extracts text from found sources."""
        print(f"🔍 WebSearchTool received query: {query}")
        results = search_and_extract(query, num_results=5)
        return "\n\n".join([f"Source: {res['url']}\n{res['text']}" for res in results])

    def _arun(self, query: str) -> str:
        """Async version fallback."""
        return self._run(query)
