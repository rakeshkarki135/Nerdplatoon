import requests
import json
from bs4 import BeautifulSoup


def get_all_data():
     url = "https://precondo.ca/wp-admin/admin-ajax.php"
     querystring = {
          "action": "list_listing",
          "filter[]": ["843", "842", "844"],
          "term": "163",
          "r": "0.5926595323295705",
          "test": "1",
          "af[unitrange][0]": "0",
          "af[unitrange][1]": "100603",
          "af[pricerange][0]": "0",
          "af[pricerange][1]": "25000000",
          "af[pricesqft][0]": "0",
          "af[pricesqft][1]": "9020",
          "af[ctype][]": ["studio", "1_bed", "1_plus_den", "2_bed", "2_plus_den", "3_bed", "more"],
     }

     headers = {
          "accept": "application/json, text/javascript, */*; q=0.01",
          "accept-language": "en-US,en;q=0.8",
          "referer": "https://precondo.ca/new-condos-toronto/",
          "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
          "x-requested-with": "XMLHttpRequest",
     }

     all_data = []
     current_page = 1

     while True:
          querystring["paged"] = current_page
          response = requests.get(url, headers=headers, params=querystring)

          if response.status_code != 200:
               print(f"Status: {response.status_code} for page: {current_page}")
               current_page += 1
               continue
               

          try:
               json_data = response.json()
               data = json_data.get("map", [])
               html_content = json_data.get("page", "")

               if not data:
                    print(f"No data found on page {current_page}")
                    break

               all_data.extend(data)

               # Find next page link
               soup = BeautifulSoup(html_content, "lxml")
               next_page_element = soup.find("a", class_="page-numbers", string=str(current_page + 1))
               print("nxt_page  " , next_page_element)

               if not next_page_element:
                    print(f"Next page element not found. Current-page {current_page}.")
                    current_page += 1
                    continue

               print(f"Getting data from page {current_page}, total records: {len(all_data)}")
               current_page += 1

          except Exception as e:
               print(f"Error processing data: {e}")
               break

     print("All data retrieved.")
     with open("data.json", "w") as file:
          json.dump(all_data, file, indent=4)

     return all_data


def main():
     get_all_data()


if __name__ == "__main__":
     main()
