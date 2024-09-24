
def countryDivider(countryList):
     divider = (len(countryList)+1)//2
     list1 = countryList[:divider]
     list2 = countryList[divider:]

     return list1,list2

     country_list = ["india","china","nepal","indonesia","malayasia","japan","tahiland"]

print(countryDivider(country_list))