import pandas as pd 

from selenium import webdriver
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC   
from bs4 import BeautifulSoup


def webdriver_Initialization():
     driver = webdriver.Chrome()
     driver.maximize_window()
     return driver


def url_Scraper(driver, link):
     urls = []
     
     while True:
          driver.get(link)
          
          WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.has-ingrid.grid__item')))
          
          soup = BeautifulSoup(driver.page_source, 'lxml')
          # print(soup)
          
          try:
               container = soup.find('div', class_ = 'has-ingrid grid__item')
               if container:
                    boxes = container.find_all('div', class_ = 'default--1-2 desk-large--1-3 desk-wide--1-3 lap-wide--1-2 lap--1-1 palm-wide--1-1 palm--1-1 grid__item')
                    # print(len(boxes))
                    
                    for box in boxes:
                         link_element = box.find('a')
                         
                         if link_element:
                              url = 'https://www.hgchristie.com' + link_element.get('href')
                              urls.append(url)
                         else:
                              print('No link element')
                              
          except Exception as e:
               print(f'Error while getting container : {e}')
               return

          # for nextPage
          try:
               next_con = soup.find('div', id='paging_bottom')
               if next_con:
                    next_element = soup.find('a', {"aria-label":"Next Page"})
                    if next_element:
                         link = 'https://www.hgchristie.com' + next_element.get('href')
                         print(link)
               else:
                    break  
          except Exception as e:
               print(f'Error while getting link container : {e}')
               
     return urls

# to run multiple links
def multiple_Links_Runner(links, driver):
     all_urls = []
     for link in links:
          urls = url_Scraper(driver, link)
          all_urls.extend(urls)
          
     return all_urls
     
# Main Function
def main():
     driver = webdriver_Initialization()
     
     links = ['https://www.hgchristie.com/eng/sales/new-listings-sort','https://www.hgchristie.com/eng/sales/old-listings-sort','https://www.hgchristie.com/eng/rentals/new-listings-sort','https://www.hgchristie.com/eng/rentals/old-listings-sort']
     
     urls =  multiple_Links_Runner(links, driver)
     
     driver.quit()
     
     df = pd.DataFrame(urls, columns = ['link'])
     
     df.to_csv('urls.csv', index=False)
     
     print('Scraping completed')
     
     
if __name__  == '__main__':
     main()