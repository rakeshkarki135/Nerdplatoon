import requests 

urls = ['https://remax-central.com.sv/en/properties/oasis-residence-model-a---3-rooms-barra-de-santiago-el-salvador',
          'https://www.hgchristie.com/eng/sales/detail/529-l-82274-f1396253027/mackey-street-and-clarke-la-mackey-street-np']

for url in urls:
     try:
          response = requests.get(url)
          print(url)
          print(response.status_code)
     except Exception as e:
          print(f'Error : {e}')