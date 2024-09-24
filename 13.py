def uniqueCheck(listobject):
     for i in listobject:
     count = listobject.count(i)
     if count > 1:
          return False
     return True

print(uniqueCheck(["hari","ram","sham"]))