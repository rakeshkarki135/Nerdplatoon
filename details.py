import requests
import pandas as pd
from bs4 import BeautifulSoup



def soup_creator(url):
     try:
          response = requests.get(url)
          print(response.status_code)
          html_content = response.content
          soup = BeautifulSoup(html_content, 'lxml')
          main_container = soup.find('div', class_ = 'container my-4')          
          return main_container
     
     except Exception as e:
          print(f"Error while getting main container : {e}")
          return None


def image(soup):
     try:
          img_container = soup.find('div', class_ = 'image-gallery grid-1')
          
          img_src = []
          if img_container:
               img_elements = img_container.find_all('a', class_ = 'popup-image')
               
               if img_elements is not None:
                    for item in img_elements:
                         img = item.get('href')
                         img_src.append(img)
                    # print(img_src)
          
          return img_src
     
     except Exception as e:
          print(f"Error while getting images : {e}")
          
          
def title_and_location(soup):
     try:
          info_container = soup.find('div', class_ = 'property-title')
          
          if info_container:
               # for Title
               title_element = info_container.find('h1')
               title = title_element.text.strip() if title_element else None
               
               # for location
               location_element = info_container.find('p', class_ = 'address-img fs-6')
               location = location_element.text.strip() if location_element else None
               
     
          return title, location
               
     except Exception as e:
          print(f"Error while getting Title and Location : {e}")

def Overview(soup):
     try:
          overview_con = soup.find('div', class_ = 'overview')
          boxes = overview_con.find_all('div', class_ = 'overview-item')
          overview_obj = {} 
          for box in boxes:
               data_element = box.find('span')
               
               if data_element:
                    values = data_element.text.split()
                    key = values[0].lower()
                    value = values[1]
                    overview_obj[key] = value
                    
          print(overview_obj)     
     except Exception as e:
          print(f"Error whle getting overview details : {e}")
     


def url_handler(df):
     urls = df['link'].tolist()
     
     for i,url in enumerate(urls):
          print(i+1, url)
          soup = soup_creator(url)
          img_src, title_location, overview =  functions_handler(soup, image, title_and_location, Overview)
          print(img_src)
          print(title_location[0])
          break
     
     
def functions_handler(soup, *functions):
     results = []
     for func in functions:
          results.append(func(soup))
     
     return results
     
     
     
def main():
     urls_df = pd.read_csv('urls.csv')
     
     url_handler(urls_df)
     
     
if __name__ == '__main__':
     main()


