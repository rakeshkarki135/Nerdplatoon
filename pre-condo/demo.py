import requests
import json
import random
import pandas as pd

from bs4 import BeautifulSoup


url = "https://precondo.ca/wp-admin/admin-ajax.php"

querystring = {
     "action": "list_listing",
     "filter[]": "843"
     }

headers = {
     "accept": "application/json, text/javascript, */*; q=0.01",
     "accept-language": "en-US,en;q=0.8",
     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
     "x-requested-with": "XMLHttpRequest",
     }

cities =  {
     "ajax" : {
          "referer":"https://precondo.ca/new-condos-ajax/",
          "term":"954" 
     },

     "aurora" : {
          "referer":"https://precondo.ca/new-condos-aurora/",
          "term":"1263"
     },

     "barrie" : {
          "referer":"https://precondo.ca/new-condos-barrie/",
          "term":"498"
     },

     "bowmanville" : {
          "referer":"https://precondo.ca/new-condos-bowmanville/",
          "term":"982"
     },

     "brampton" : {
          "referer":"https://precondo.ca/new-condos-brampton/",
          "term":"255"
     },

     "burlington" : {
          "referer":"https://precondo.ca/new-condos-burlington/",
          "term":"171"
     },

     "calendon" : {
          "referer":"https://precondo.ca/new-condos-caledon/",
          "term":"885"
     },

     "calgary-alberta" : {
          "referer":"https://precondo.ca/new-condos-calgary-alberta/",
          "term":"1405"
     },

     "cambridge" : {
          "referer":"https://precondo.ca/new-condos-cambridge/",
          "term":"1803"
     },

     "cobourg" : {
          "referer":"https://precondo.ca/new-condos-cobourg/",
          "term":"1225"
     },

     "collingwood" : {
          "referer":"https://precondo.ca/new-condos-collingwood/",
          "term":"705"
     },

     "the-blue-mountains" : {
          "referer":"https://precondo.ca/new-condos-tcc/",
          "term":"992"
     },

     "edmonton-alberta" : {
          "referer":"https://precondo.ca/new-condos-edmonton-alberta/",
          "term":"1739"
     },

     "etobicoke" : {
          "referer":"https://precondo.ca/new-condos-etobicoke/",
          "term":"164"
     },

     "central-etobicoke" : {
          "referer":"https://precondo.ca/new-condos-central-etobicoke/",
          "term":"173"
     },

     "mimico" : {
          "referer":"https://precondo.ca/new-condos-mimico/",
          "term":"172"
     },

     "guelph" : {
          "referer":"https://precondo.ca/new-condos-guelph/",
          "term":"1272"
     },

     "halton-hills" : {
          "referer":"https://precondo.ca/new-condos-halton-hills/",
          "term":"1793"
     },

     "hamilton" : {
          "referer":"https://precondo.ca/new-condos-hamilton/",
          "term":"179"
     },


     "ancaster" : {
          "referer":"https://precondo.ca/new-condos-ancaster/",
          "term":"805"
     },

     "grimsby" : {
          "referer":"https://precondo.ca/new-condos-grimsby/",
          "term":"993"
     },

     "huntsville" : {
          "referer":"https://precondo.ca/new-condos-huntsville/",
          "term":"720"
     },

     "innisfil" : {
          "referer":"https://precondo.ca/new-condos-innisfil/",
          "term":"924"
     },

     "king-city" : {
          "referer":"https://precondo.ca/new-condos-king-city/",
          "term":"1815"
     },

     "kitchener" : {
          "referer":"https://precondo.ca/new-condos-kitchener/",
          "term":"941"
     },

     "laval" : {
          "referer":"https://precondo.ca/new-condos-laval/",
          "term":"1306"
     },

     "london" : {
          "referer":"https://precondo.ca/new-condos-london/",
          "term":"1053"
     },

     "markham" : {
          "referer":"https://precondo.ca/new-condos-markham/",
          "term":"196"
     },

     "milton" : {
          "referer":"https://precondo.ca/new-condos-milton/",
          "term":"996"
     },

     "mississauga" : {
          "referer":"https://precondo.ca/new-condos-mississauga/",
          "term":"166"
     },

     "erin-mills" : {
          "referer":"https://precondo.ca/new-condos-erin-mills/",
          "term":"183"
     },

     "port-credit/" : {
          "referer":"https://precondo.ca/new-condos-port-credit/",
          "term":"184"
     },

     "square-one" : {
          "referer":"https://precondo.ca/new-condos-square-one/",
          "term":"182"
     },

     "montreal" : {
          "referer":"https://precondo.ca/new-condos-montreal/",
          "term":"491"
     },


     "mount-royal": { 
          "referer": "https://precondo.ca/new-condos-mount-royal/",
          "term": "1244"
     },
     
     "newmarket" : {
          "referer": "https://precondo.ca/new-condos-newmarket/",
          "term": "717"
     },

     "niagara-falls" : {
          "referer": "https://precondo.ca/new-condos-niagara-falls/",
          "term": "1257"   
     },

     "oakville" : {
          "referer": "https://precondo.ca/new-condos-oakville/",         
          "term": "170s"
     },

     "orillia" : {
          "referer": "https://precondo.ca/new-condos-orillia/",
          "term": "1821"
     },

     "oshawa" : {
          "referer": "https://precondo.ca/new-condos-oshawa/",
          "term": "368"
     },

     "courtice" : {
          "referer": "https://precondo.ca/new-condos-courtice/",
          "term": "686"
     },

     "pickering" : {
          "referer": "https://precondo.ca/new-condos-pickering/",
          "term": "467"
               
     },

     "pointe-claire" : {
          "referer": "https://precondo.ca/new-condos-pointe-claire/",                
          "term": "1243"
               
     },

     "richmond-hill" : {
          "referer": "https://precondo.ca/new-condos-richmond-hill/",
          "term" : "168",
     
     },

     "scarborough" : {
          "referer": "https://precondo.ca/new-condos-scarborough/",
          "term" : "167"
     },

     "st-catharines" : {
          "referer": "https://precondo.ca/new-condos-st-catharines/",
          "term" : "1534"
     },

     "stratford" : {
          "referer": "https://precondo.ca/new-condos-stratford/",
          "term": "1798"
          
     },

     "thornhill" : {
          "referer": "https://precondo.ca/new-condos-thornhill/",
          "term" : "801"
     
     },

     "toronto" : {
     "referer": "https://precondo.ca/new-condos-toronto/",
     "term" :"163"
     
     },


     "don-mills-and-eglinton": {
          "referer": "https://precondo.ca/new-condos-don-mills-and-eglinton/",
          "term": "259"
     },
          
          
     "downtown-toronto" : {
          "referer": "https://precondo.ca/new-condos-downtown-toronto/",
          "term" :"174"
     },

     "east" : {
          "referer": "https://precondo.ca/new-condos-downtown-toronto-east/",
          "term" : "232"
          
     },

     "west" : {
          "referer":"https://precondo.ca/new-condos-king-west/",
          "term": "177"      
     },

     "riverdale" : {
          "referer": "https://precondo.ca/new-condos-leslieville-riverdale/",
          "term" : "217"
          
     },

     "liberty" : {
          "referer":"https://precondo.ca/new-condos-liberty-village/",
          "term":"180"
     },

     "midtown" : {
          "referer":"https://precondo.ca/new-condos-midtown/",
          "term":"181"
          
     },
     
     "northYork" : {
          "referer": "https://precondo.ca/new-condos-north-york/",
          "term": "178",

     },

     "Beaches" : {
          "referer": "https://precondo.ca/new-condos-the-beaches/",
          "term":"302"
          
     },

     "waterfront" : {
          "referer": "https://precondo.ca/new-condos-toronto-waterfront/",
          "term": "176"
     },

     "west-toronto" : {
          "referer": "https://precondo.ca/new-condos-west-toronto/",
          "term": "319"
          
     },

     "eglinton" : {
          "referer": "https://precondo.ca/new-condos-yonge-and-eglinton/",
          "term" : "236"
          
     },

     "yorkdale" : {
          "referer":"https://precondo.ca/new-condos-yorkdale/",
          "term":"328"
     },

     "yorkville" : {
          "referer": "https://precondo.ca/new-condos-yorkville/",
          "term":"175"
          
     },

     "uxbridge" : {
          "referer": "https://precondo.ca/new-condos-uxbridge/",
          "term":"715"
          
     },

     "vaughan" : {
          "referer":"https://precondo.ca/new-condos-vaughan/",
          "term" : "165"
          
     },

     "woodbridge" : {
          "referer":"https://precondo.ca/new-condos-woodbridge/",
          "term":"317"
          
     },

     "wasaga-beach" : {
          "referer": "https://precondo.ca/new-condos-wasaga-beach/",
          "term": "1262"
          
     },

     "waterloo" : {
          "referer": "https://precondo.ca/new-condos-waterloo/",
          "term" : "942"
          
     },

     "wellland" : {
          "referer": "https://precondo.ca/new-condos-welland/",
          "term" : "1004"
          
     },

     "whitby" : {
          "referer": "https://precondo.ca/new-condos-whitby/",
          "term" :"950"
          
     },
}   


def dynamic_url_generator(cities : dict) -> list:
     all_data = []
     for city,details in cities.items():
          current_page = 1
          while True:
               querystring["paged"] = current_page
               querystring["r"] = random.uniform(0.0, 0.99)
               querystring["term"] = details.get('term')
               headers["referer"] = details.get('referer')
               
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
                         print(f"No data found on page - {current_page} from link {headers['referer']}")
                         break
                    
                    all_data.extend(data)
                    print(f"Fetched data from page {current_page}, total records: {len(all_data)}, on {headers['referer']}")

                    # Find next page link
                    soup = BeautifulSoup(html_content, "lxml")
                    next_page_element = soup.find("a", class_="page-numbers", string=str(current_page + 1))

                    if not next_page_element:
                         print(f"Next page element not found. Current-page {current_page}.")
                         print("")
                         break

                    current_page += 1

               except Exception as e:
                    print(f"Error processing data: {e}")
                    break

     with open("data.json", "w") as file:
          json.dump(all_data, file, indent=4)

     return all_data