def typecheck(listObject):
     first = listObject[0]
     index = type(first)
     for i in listObject:
          if not isinstance(i, index):
               return False
     return True

list1 = [1,2,3,4,5,6,7]
list2 = ['hindi',2,4,'china']

print(typecheck(list1))
print(typecheck(list2))