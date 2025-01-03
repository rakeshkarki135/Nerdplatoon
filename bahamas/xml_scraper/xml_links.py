import pandas as pd
import logging
from bs4 import BeautifulSoup

from base.log_config import dictConfig
logger = logging.getLogger("links")


def soup_creator(xml_filename):
    with open(xml_filename, 'r', encoding='utf-8') as file:
        xml_content = file.read()

    soup = BeautifulSoup(xml_content, "xml")
    if not soup:
        logger.error("soup is not found")
        return 
    
    return soup
    

def url_extractor(soup):
    try:
        urls = []
        url_elements = soup.find_all("xhtml:link", {"hreflang":"en"})
        
        if url_elements:
            for url_element in url_elements:
                    url = url_element.get("href")
                    urls.append(url)
                
        return urls
    except Exception as e:
        logger.error("Failed to extract links", exc_info=e)
    
    
def main():
    xml_file_names = ["./xml_files/sitemap_4.xml","./xml_files/sitemap_5.xml","./xml_files/sitemap_6.xml","./xml_files/sitemap_8.xml"]
    
    for name in xml_file_names:
        soup = soup_creator(name)
        
        urls = url_extractor(soup)
        
        if len(urls) > 1:
            df = pd.DataFrame(urls, columns=['url'])
            df = df.drop_duplicates(subset=['url'], keep='first')
            # Save the DataFrame to a CSV file
            df.to_csv(f"{name}demo.csv", index=False)
            
            logger.info(f"Links extracted from ---> {name}")
            
        else:
            logger.info(f"No data to create csv files in  --> {name}")

    
    
if __name__ == "__main__":
    main()