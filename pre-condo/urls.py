import requests  
import pandas as pd 
from bs4 import BeautifulSoup



def soup_creator(url):
     response = requests.get(url)
     html_content = response.content
     soup = BeautifulSoup(html_content, 'lxml')
     return soup
     
     
def url_scraper(soup):
     try:
          main_container = soup.find('div', id='loop')
          if main_container:
               box_container = main_container.find('div', class_ =  'container')
               links = []
               
               if box_container:
                    link_elements = box_container.find_all('a', class_ = 'd-block position-relative overflow-hidden')
                    for item in link_elements:
                         link = item.get('href')
                         links.append(link)
                    
                    # print(links)
                    
               # for next page 
               next_page_container = soup.find('nav', class_ = 'navigation pagination')
               if next_page_container:
                    next_page_element = next_page_container.find('a', class_ = 'next page-numbers')
                    
                    if next_page_element:
                         url = next_page_element.get('href')
                    else:
                         url = None
                    
          
          return links, url
     except Exception as e:
          print(f"Error while getting links")
          


def main():
     url = "https://precondo.ca/?s=all"
     links=[]
     
     while True:
          try:
               print(url)
               soup = soup_creator(url)
               
               link, url = url_scraper(soup)
               links.extend(link)
               
          except Exception as e:
               print(f"All urls Extracted : {e}")
               break
          
     df = pd.DataFrame(links, columns = ['link'])
     df.to_csv('urls.csv', index=False)
     
     
if __name__ == '__main__':
     main()