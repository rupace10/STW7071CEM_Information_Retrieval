import os
import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser

def extract_publication_info(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all publication containers
        publication_containers = soup.find_all("div", class_="result-container")

        # Iterate over each publication container
        for container in publication_containers:
            # Extract the title
            title_tag = container.find("h3", class_="title")
            title = title_tag.text.strip() if title_tag else None

            # Extract the anchor tag and its href
            anchor_tag = title_tag.find("a") if title_tag else None
            anchor_url = anchor_tag['href'] if anchor_tag and 'href' in anchor_tag.attrs else None

            # Extract authors
            authors_tags = container.find_all("a", rel="Person")
            authors = [author.text.strip() for author in authors_tags] if authors_tags else None

            # Extract the year
            year_tag = container.find("span", class_="date")
            year = year_tag.text.strip() if year_tag else None

            # Print the extracted information
            print("Title:", title)
            print("URL:", anchor_url)
            print("Authors:", ", ".join(authors))
            print("Year:", year)
            print("-----------------------")

# URL of the webpage
url = "https://pureportal.coventry.ac.uk/en/organisations/ihw-centre-for-health-and-life-sciences-chls"

# Call the function to extract publication information
extract_publication_info(url)
