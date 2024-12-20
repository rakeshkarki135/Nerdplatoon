import requests    
import logging
import pandas as pd

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from base.log_config import dictConfig
logger = logging.getLogger("link_logger")


def soup_creator(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        logger.error(f"Failed to get the page ---> {response.status_code}")
        return 

    soup = BeautifulSoup(response.content, "lxml")
    main_container = soup.find("div", class_ = "breakpoint active")
    
    if not main_container:
        logger.error("Failed to create the soup, Main container not found")
        return 
    
    container = main_container.find("div", id="u4939")
    
    if not container:
        logger.error("Failed to create soup, Container not found")
        return 
    
    return container
    
    

def link_extractor(soup):
    base_url = "https://mesora.org"
    links = []
    titles = []
    seen_links = set()  # A set to track unique links
    items = []
    
    try:
        table = soup.find("table", class_="Times2")
        
        if table:
            table_rows = table.find_all("tr")
            
            for row in table_rows:
                list_items = row.find_all("li")
                
                for item in list_items:
                    link_element = item.find("a")
                    title = item.get_text(strip=True)  # Extract clean title text
                    
                    if link_element:
                        raw_link = link_element.get('href')
                        
                        if raw_link:  # Ensure the link is not None or empty
                            # Normalize the link using urljoin
                            link = urljoin(base_url, raw_link)
                            
                            # Check for duplicates using the seen_links set
                            if link not in seen_links:
                                seen_links.add(link)  # Add the link to the set
                                links.append(link)  # Append unique link to the list
                                titles.append(title)  # Append title to titles list
                                items.append({"title": title, "link": link})
        
        return items  # Return a list of dictionaries for better structure
    
    except Exception as e:
        logger.error("Something went wrong while extracting links and titles", exc_info=e)
        return []



def main():
    url = "https://mesora.org/philosophy.html"
    
    soup = soup_creator(url)
    
    items = link_extractor(soup)
    
    df = pd.DataFrame(items)
    
    df.to_csv("links.csv")
    
    
if __name__ == "__main__":
    main()