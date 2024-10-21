import requests
import json
import pandas as pd   


def url_extractor():
     url = "https://cuuo4s.a.searchspring.io/api/search/search.json"

     querystring = {"ajaxCatalog":"v3","resultsFormat":"native","siteId":"cuuo4s","domain":"https://houseofrohl.com/kitchen/faucets/#/perpage:500","bgfilter.categories_hierarchy":"Kitchen>Faucets","resultsPerPage":"500","q":"","userId":"363a720a-3a94-4947-a0fe-6054121b7a4c","sessionId":"c701f609-a60b-4f2c-b762-5cc4501d4002","pageLoadId":"4ea077ed-f15d-4af1-b14b-b60cd0bb98d4","lastViewed":["A3318ILAPC2","CU51LPN2","CU51LAPC2"],"bgfilter.ss_disabled":"0"}

     payload = ""
     headers = {
     "accept": "application/json, text/plain, */*",
     "accept-language": "en-US,en;q=0.8",
     "origin": "https://houseofrohl.com",
     "priority": "u=1, i",
     "referer": "https://houseofrohl.com/",
     "sec-ch-ua": '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
     "sec-ch-ua-mobile": "?1",
     "sec-ch-ua-platform": '"Android"',
     "sec-fetch-dest": "empty",
     "sec-fetch-mode": "cors",
     "sec-fetch-site": "cross-site",
     "sec-gpc": "1",
     "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36"
     }

     response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

     data = response.json()

     res = []
     for x in data['results']:
          url = 'https://houseofrohl.com' + x['url']
          res.append(url)

     df = pd.DataFrame(res, columns=['URL'])
     # print(df)
     df.to_csv('urls.csv', index=False)


if  __name__ == '__main__':
     url_extractor()
     
