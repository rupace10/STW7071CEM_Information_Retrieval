import os
import requests
from bs4 import BeautifulSoup
from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD, ID
from whoosh.qparser import QueryParser

# Function to crawl and scrape publication data from the provided URL
def crawl_and_scrape(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    publications = []

    # Extract publication details from the webpage
    for container in soup.find_all('div', class_='result-container'):
        title_tag = container.find("h3", class_="title")
        title = title_tag.text.strip() if title_tag else None

        # Extract the publication_link tag and its href
        anchor_tag = title_tag.find("a") if title_tag else None
        publication_link = anchor_tag['href'] if anchor_tag and 'href' in anchor_tag.attrs else None

        # Extract authors
        authors = [author.text.strip() for author in container.find_all('a', rel="Person")]

        # Extract the year
        year_tag = container.find("span", class_="date")
        publication_year = year_tag.text.strip() if year_tag else None

        publications.append({
            'title': title,
            'authors': authors,
            'publication_year': publication_year,
            'publication_link': publication_link
        })

    return publications

# Function to create or open the Whoosh index
def get_index():
    schema = Schema(
        title=TEXT(stored=True),
        authors=TEXT(stored=True),
        publication_year=ID(stored=True),
        publication_link=ID(stored=True)
    )

    directory = "index"
    if not os.path.exists(directory):
        os.mkdir(directory)
    
    ix = index.create_in(directory, schema)
    return ix

# Function to index the crawled publication data
def index_publications(ix, publications):
    writer = ix.writer()

    for publication in publications:
        writer.add_document(
            title=publication['title'],
            authors=",".join(publication['authors']),
            publication_year=publication['publication_year'],
            publication_link=publication['publication_link']
        )

    writer.commit()

# Function to search the index
def search_index(query_str):
    directory = "index"
    ix = index.open_dir(directory)
    results = []

    with ix.searcher() as searcher:
        query_parser = QueryParser("title", ix.schema)
        query = query_parser.parse(query_str)
        hits = searcher.search(query, limit=None)
        
        for hit in hits:
            fields = hit.fields()
            title = fields.get('title', 'N/A')  # Handle missing fields gracefully
            authors = fields.get('authors', 'N/A')
            publication_year = fields.get('publication_year', 'N/A')
            publication_link = fields.get('publication_link', 'N/A')

            results.append({
                'title': title,
                'authors': authors,
                'publication_year': publication_year,
                'publication_link': publication_link
            })

    return results
