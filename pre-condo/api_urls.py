import requests
import json
import random
import pandas as pd

from bs4 import BeautifulSoup
from urls_api_config import dynamic_url_generator, cities, url


def get_all_data():
     all_data = []
     
     # Generate dynamic URLs, headers, and query strings
     dynamic_urls = dynamic_url_generator(cities)

     for dynamic_config in dynamic_urls:
          city_name = dynamic_config["city"]
          dynamic_headers = dynamic_config["headers"]
          dynamic_querystring = dynamic_config["querystring"]

          # print(f"Fetching data for city: {city_name}")
          try:
               # Make the request with dynamic headers and query string
               response = requests.get(url, headers=dynamic_headers, params=dynamic_querystring)
               
               # Check response status
               if response.status_code != 200:
                    print(f"Error: Received status {response.status_code} for city {city_name}")
                    continue

               # Parse JSON response
               json_data = response.json()
               data = json_data.get("map", [])
               html_content = json_data.get("page", "")

               # If no data found, log and continue
               if not data:
                    print(f"No data found for city: {city_name}")
                    continue

               # Extend all_data with the fetched records
               all_data.extend(data)
               print(f"Fetched {len(data)} records for city: {city_name}, Total: {len(all_data)}")
               print("")

          except Exception as e:
               print(f"Error fetching data for city {city_name}: {e}")
               continue

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
     extracted_json = get_all_data()
     links = urls_extractor(extracted_json)
     
     df = pd.DataFrame(links, columns = ['link'])
     df.to_csv('api_urls.csv', index=False)

     print("All links Extracted.")
     
     
     
if __name__ == "__main__":
     main()
