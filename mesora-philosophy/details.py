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

def remove_attributes(element):
    for tag in element.find_all(True):
        tag.attrs = {}
    return element

def detail_extractor(soup):
    dt_tags = soup.find_all('dt')
    
    dt_texts = []
    
    for dt in dt_tags:
        # Get the inner HTML of each <dt> tag using .decode_contents(), which preserves inner HTML tags
        dt_contents = dt.decode_contents()  
        
        # Append the cleaned content to the list (this keeps all inner tags intact)
        dt_texts.append(dt_contents)
    
    # Join the results with new lines for readability
    result_text = '\n'.join(dt_texts)
    # print(result_text)
    
    return result_text


def multiple_link_runner():
    df = pd.read_csv("links.csv")
    links = df['link'].tolist()
    # links=["https://mesora.org/intermarriage.html"]
    
    about = []
    if len(links) > 0:
        for link in links:
            soup = soup_creater(link)
            output = detail_extractor(soup)
            about.append(output)
            
    return {
        "about":about
    }

def main():
    about = multiple_link_runner()
    
    df = pd.DataFrame(about)
    
    df.to_csv("detail.csv", index=False)
    
    


if __name__ == "__main__":
    main()
