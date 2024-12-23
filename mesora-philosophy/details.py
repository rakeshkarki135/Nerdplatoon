import requests 
import pandas as pd
from bs4 import BeautifulSoup

from logging import getLogger
logger = getLogger("details")

def soup_creater(url):
    response = requests.get(url)
    html_response = response.content
    soup = BeautifulSoup(html_response, "lxml")
    return soup


def detail_extractor(soup):
    details = soup.find("dl")
    
    if details:
        cleaned_details = remove_attributes
        


def multiple_link_runner():
    df = pd.read_csv("links.csv")
    # links = df['link'].tolist()
    links=["https://mesora.org/intermarriage.html"]
    
    if len(links) > 0:
        for link in links:
            soup = soup_creater(link)
            detail_extractor(soup)
            break
    

def main():
    multiple_link_runner()
    
    


if __name__ == "__main__":
    main()
