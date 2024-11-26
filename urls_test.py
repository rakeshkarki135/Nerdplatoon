import requests
import json
import random
import pandas as pd

from bs4 import BeautifulSoup


def get_all_data():
     url = "https://precondo.ca/wp-admin/admin-ajax.php"
     querystring = {
          "action": "list_listing",
          "filter[]": "843",
          "term": "163",
          "r": "0.5926595323295705",
          "test": "1"
     }

     headers = {
          "accept": "application/json, text/javascript, */*; q=0.01",
          "accept-language": "en-US,en;q=0.8",
          "referer": "https://precondo.ca/",
          "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
          "x-requested-with": "XMLHttpRequest",
     }

     all_data = []
     current_page = 1

     while True:
          querystring["paged"] = current_page
          querystring["r"] = random.uniform(0.0, 0.99)
          response = requests.get(url, headers=headers, params=querystring)

          if response.status_code != 200:
               print(f"Status: {response.status_code} for page: {current_page}")
               current_page += 1
               continue
               
          try:
               json_data = response.json()
               data = json_data.get("map", [])
               html_content = json_data.get("page", "")

               if len(data) == 0:
                    print(f"No data found on page - {current_page}")
                    break
               
               all_data.extend(data)
               print(f"Fetched data from page {current_page}, total records: {len(all_data)}")

               # Find next page link
               soup = BeautifulSoup(html_content, "lxml")
               next_page_element = soup.find("a", class_="page-numbers", string=str(current_page + 1))

               if not next_page_element:
                    print(f"Next page element not found. Current-page {current_page}.")
                    break

               current_page += 1

          except Exception as e:
               print(f"Error processing data: {e}")
               break
     
     with open("data.json", "w") as file:
          json.dump(all_data, file, indent=4)

     return all_data

def urls_extractor(extracted_json):
     links = []
     for item in extracted_json:
          html_content = item.get('html', None)
          
          if html_content is not None:
               soup = BeautifulSoup(html_content, 'lxml')
               link_element = soup.find('a', class_ = 'btn')
               
               if link_element:
                    link = link_element.get('href')
                    links.append(link)
     # print(links)
     return links


def main():
     extracted_josn = get_all_data()
     links = urls_extractor(extracted_josn)
     
     df = pd.DataFrame(links, columns = ['link'])
     df.to_csv('api_urls.csv', index=False)

     print("All data retrieved.")
     
     
     
if __name__ == "__main__":
     main()
