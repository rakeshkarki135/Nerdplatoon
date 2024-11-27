import requests
import json
import random
import pandas as pd

from time import sleep
from bs4 import BeautifulSoup
from urls_api_config import dynamic_url_generator, cities, url


def get_all_data():
     all_datas = []
     
     # Generate dynamic URLs, headers, and query strings
     dynamic_urls = dynamic_url_generator(cities)

     for  dynamic_config in dynamic_urls:
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

               # If no data found, log and continue
               if not data:
                    print(f"No data found for city: {city_name}")
                    continue

               # Extend all_data with the fetched records
               all_datas.extend(data)
               print(f"Fetched data of city --> {city_name}, Total --> {len(all_datas)}, link --> {dynamic_headers['referer']}")
               print("")

          except Exception as e:
               print(f"Error fetching data for city {city_name}: {e}")
               continue

     return all_datas



def urls_extractor(extracted_json):
     links = []
     lats = []
     lons = []
     location_flags = []
     for item in extracted_json:
          html_content = item.get('html', None)
          
          if html_content is not None:
               soup = BeautifulSoup(html_content, 'lxml')
               link_element = soup.find('a', class_ = 'btn')
               
               if link_element:
                    link = link_element.get('href')
                    links.append(link)

     
          lat = item.get('lat', None)
          lats.append(lat)
          lon = item.get('lon', None)
          lons.append(lon)

          

          if lat is None or lon is None:
               location_flag  = 0
               location_flags.append(location_flag)
               
          else:
               location_flag = 1
               location_flags.append(location_flag)
               

     # print(links)
     return links, lats, lons, location_flags


def main():
     extracted_json = get_all_data()
     links, lats, lons, location_flags = urls_extractor(extracted_json)
     
     df = pd.DataFrame(links,lats,lons,location_flags, columns = ['link','lat','lon','location_flag'])

     df.drop_duplicates(subset="link", keep="first", inplace=True)
     
     df.to_csv('api_urls.csv', index=False)

     print("All links Extracted.")
     
     
     
if __name__ == "__main__":
     main()
