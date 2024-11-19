
def detail_extractor(link):
     try:
          price = img_urls = about = partial_baths = full_baths = bedrooms = property_type = exterior = interior = property_details = interior_details = exterior_details = amnities_list = new_features =  None
          
          driver = driver_initialization()
          driver.get(link)
          
          WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.grid.global-content.js-global-content')))
          
          soup = BeautifulSoup(driver.page_source, 'lxml')
          
          # for price
          try:
               main_container = soup.find('div', class_ = 'grid global-content js-global-content')
               if  main_container:
                    head_con = soup.find('div', id='listingtitle')
                    
                    if head_con:
                         # for price 
                         price_con = head_con.find('div', class_ = 'c-price')
                         if price_con:
                              price_element = price_con.find('span')
                              
                              if price_element:
                                   price = price_element.get_text(strip=True)
                                   price = ''.join(re.findall(r'\d+', price))
                              else:
                                   price = None
                    
          except Exception as e:
               print(f'Error while getting price : {e}')
               
               
          # for propertyDetail
          try:
               main_propDetail_con = soup.find('div', id='listinginfo')
               if main_propDetail_con:
                    propDetail_con = main_propDetail_con.find('div', class_='grid__item')
                    
                    if propDetail_con:
                         propertyDetails = {}
                         propDetail_boxes = propDetail_con.find_all('div', {'data-same-height-group':'listinginfo'})

                         for box in propDetail_boxes:
                              key_element = box.find('dt', class_ = 'listing-info__title')
                              value_element = box.find('dd', class_ = 'listing-info__value')
                              
                              if key_element and value_element:
                                   key = key_element.get_text(strip=True)
                                   value = value_element.get_text(strip=True)
                                   
                                   if key in ['Full Baths', 'Full Bath']:
                                        full_baths = value
                                   elif key in ['Partial Baths', 'Partial Bath']: 
                                        partial_baths =  value
                                   elif key in ['Bedrooms','Bedroom']:
                                        bedrooms = value
                                   else:
                                        if key == 'Interior':
                                             value = ''.join(re.findall(r'\d+', value))
                                             interior = value
                                        if key == 'Exterior':
                                             value = value.replace('Acres', '')
                                             exterior = value
                                        if key == 'Property Type':
                                             property_type = value
                                        
                                             
          except Exception as e:
               print(f'Error while getting  Property Details  : {e}')
               
               
          # for amenities
          amnities_list = []
          try:
               amnties_main_con = soup.find('div', id = 'listingpropertydescription')
               if amnties_main_con:
                    amnties_elements = amnties_main_con.find_all('span', class_ = 'prop-description__amenities-list-item-text')
                    # print(len(amnties_list))
                    if amnties_elements:
                         amnities_list.extend([item.get_text(strip=True) for item in amnties_elements])
                         
                    # for features
                    new_features = {}
                    features_con = amnties_main_con.find('div', class_ = 'prop-description__features-list')
                    if features_con:
                         features_boxes = features_con.find_all('div', class_ = 'grid__item')
                         for box in features_boxes:
                              key_element = box.find('dt')
                              value_element = box.find('dd')
                              
                              if key_element and value_element:
                                   key = key_element.get_text(strip=True)
                                   value = value_element.get_text(strip=True)
                                   new_features[key] = value
                    
          except Exception as e:
               print(f'Error while getting Amenities  : {e}')
          
               
          # for about
          if amnties_main_con:
               try:
                    description_con = amnties_main_con.find('div', class_ = 'p')
                    if description_con:
                         about = description_con.get_text(strip=True)
                    else:
                         about = None
                    
               except Exception as e:
                    print(f'Error while getting Description : {e}')
               
               # for exterior container 
               try:
                    exterior_con = amnties_main_con.find('div', class_ = 'prop-description__details')
               except Exception as e:
                    print(f'Error while getting exterior Container : {e}')
          
          
          # for proprety exterior details
          if exterior_con:
               try:
                    exterior_boxes = exterior_con.find_all('div', class_ = 'grid__item')
                    # print(len(exterior_boxes))
                    for box in exterior_boxes:
                         ext_title = box.find('h3', class_ = 'prop-description__title').get_text(strip=True)
                         dl_con = box.find('dl')
                         
                         exterior_detail = {}
                         
                         key_elements = dl_con.find_all('dt') if dl_con else None
                         value_elements = dl_con.find_all('dd')if dl_con else None
                         
                         for x,y in zip(key_elements,value_elements):
                              key = x.get_text(strip=True)
                              value = y.get_text(strip=True)
                              
                              if key == 'Amenities':
                                   amnities_list.append(value)
                              else:
                                   exterior_detail[key] = value
                         
                         if ext_title == 'Property Details':
                              property_details = exterior_detail
                         elif ext_title == 'Exterior':
                              exterior_details = exterior_detail   
                         elif ext_title == 'Interior':
                              interior_details = exterior_detail 
                         
               except Exception as e:
                    print(f'Error while getting Exterior Details  : {e}')
          
          
          # for image_urls
          img_urls = []
          try:
               img_carousel_con = soup.find('div', id = 'detail_photos_carousel_placeholder')
               if img_carousel_con:
                    img_con = img_carousel_con.find('div', class_ = 'runner')
                    
                    if img_con:
                         img_boxes = img_con.find_all('img')
                         
                         for box in img_boxes:
                              urls = box.get('data-image-url-format', None)
                              img_urls.append(urls)
          
          except Exception as e:
               print(f'Error while getting image urls : {e}')
          
          status_404 = 0  
          
     except Exception as e:
          print(f'Error while Extracting Details : {e}')
          price  = img_urls = about = bedrooms = full_baths = partial_bath = property_type = amnities_list = exterior_details = property_details = interior_details = new_features = interior = exterior = None
          
          status_404 = 0
          
     return price, img_urls, about, bedrooms, full_baths, partial_baths, property_type, amnities_list, exterior_details, property_details, interior_details, new_features, interior, exterior ,status_404
     