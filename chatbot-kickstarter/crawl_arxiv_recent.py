import os
import requests
from bs4 import BeautifulSoup
import re

# Set up regex pattern to match PDF URLs
pattern = re.compile(r'/pdf/(\d+\.\d+)')

# Set up base URL
base_url = "https://arxiv.org"

# Set up URL for recent papers in machine learning
url = "https://arxiv.org/list/cs.LG/recent"

# Make request to URL and get HTML response
response = requests.get(url)

# Parse HTML response with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Find all links in the HTML with an "href" attribute and store in list
links = [link.get("href") for link in soup.find_all("a")]

# Filter out links that are not strings
links_clean = [link for link in links if isinstance(link, str)]

# Find all links that match the PDF URL pattern and store in list
pdf_links = [base_url + link for link in links_clean if pattern.search(link)]

# Create folder to store downloaded PDFs
os.makedirs("./arxiv_pdfs", exist_ok=True)

# Loop through PDF links and download each one
for pdf_link in pdf_links:
    # Get the PDF filename from the URL
    pdf_filename = pdf_link.split("/")[-1]
    # Make request to PDF URL and get PDF response
    pdf_response = requests.get(pdf_link)
    # Write PDF content to file
    with open(f"./arxiv_pdfs/{pdf_filename}.pdf", "wb") as f:
        f.write(pdf_response.content)

# Print number of PDFs downloaded
print(f"Downloaded {len(pdf_links)} PDFs")
