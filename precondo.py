import requests
import json

url = "https://precondo.ca/wp-admin/admin-ajax.php"

querystring = {"action":"list_listing","filter[]":["843","842","844"],"term":"163","r":"0.38774503790432413","test":"1","af[unitrange][0]":"0","af[unitrange][1]":"100603","af[pricerange][0]":"0","af[pricerange][1]":"25000000","af[pricesqft][0]":"0","af[pricesqft][1]":"9020","af[ctype][]":["studio","1_bed","1_plus_den","2_bed","2_plus_den","3_bed","more"]}

payload = ""
headers = {
     "accept": "application/json, text/javascript, */*; q=0.01",
     "accept-language": "en-US,en;q=0.8",
     "cookie": "gclid=undefined; ac_enable_tracking=1; mmuid=2d8b53c0f9dbc369",
     "priority": "u=1, i",
     "referer": "https://precondo.ca/new-condos-toronto/",
     "sec-ch-ua": '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
     "sec-ch-ua-mobile": "?1",
     "sec-ch-ua-platform": '"Android"',
     "sec-fetch-dest": "empty",
     "sec-fetch-mode": "cors",
     "sec-fetch-site": "same-origin",
     "sec-gpc": "1",
     "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
     "x-requested-with": "XMLHttpRequest"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

try:
     json_data = response.json()
     formated_data = json.dumps(json_data, indent=4)
     print(formated_data)
except Exception as e:
     print(f"Data cannot converted into json : {e}")