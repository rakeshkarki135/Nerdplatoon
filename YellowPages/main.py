from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

def get_soup(url):
     r = requests.get(url)
     return BeautifulSoup(r.text, 'lxml')


def main_page_extraction(url):
     main_df = pd.DataFrame(columns=['Title','Link','Address'])
     
     while True:
          soup = get_soup(url)
          print(url)
          ul = soup.find('ul', class_ = 'mt-4 content-wrapper')
          boxes = ul.find_all('li', class_ = 'list-content-section')
          
          for box in boxes:
               detail_container = box.find('div', class_ = 'add-details')
               title = detail_container.find('h3', class_ = 'font-20 t400').text.strip()
               link = detail_container.find('h3', class_ = 'font-20 t400').find('a')['href']
               link = "https://www.yellowpagesnepal.com/" + link
               # print(link)
               address = detail_container.find('div', class_ = 'info-row').text.strip()
               new_df = pd.DataFrame([{'Title':title,'Link':link,'Address':address}])
               main_df = pd.concat([main_df,new_df], ignore_index=True)
               # print(address)
               # break
          # main_df.to_csv('business_data.csv')
          # main_df.to_csv('business_data.csv', index=False)
          
          next_page_container = soup.find('div', class_='paging')
          
          main_container = next_page_container.find('div', class_='d-none d-md-block')
          
          next_link = main_container.find('a', {'title':'Next'})
          
          if next_link:
               url = "https://www.yellowpagesnepal.com/" + next_link.get('href')
          else:
               break
          
     return main_df


def main():
     url1 = "https://www.yellowpagesnepal.com/agricultural-equipment-and-implements"
     df = main_page_extraction(url1)
     df['Title'] = df['Title'].str.replace(r'[\n\s]','', regex=True)

     df.to_csv('business_data.csv', index=False)
     



if __name__ == "__main__":
     main()
