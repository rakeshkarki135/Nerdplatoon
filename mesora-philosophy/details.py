import requests 
import pandas as pd
from bs4 import BeautifulSoup

from 

def soup_creater(url):
    response = requests.get(url)
    html_response = response.content
    soup = BeautifulSoup(html_response, "lxml")
    return soup


def detail_extractor(link, soup):
    pass


def multiple_link_runner():
    df = pd.read_csv("links.csv")
    links = df['link'].tolist()
    
    if len(links) > 0:
        for link in links:
            soup = soup_creater(link)
            logge
            detail_extractor(link, soup)
            break
    

def main():
    multiple_link_runner()
    
    


if __name__ == "__main__":
    main()
