def zeroCheck(x):
     return x**2 + 6*x + 9


for i in range(-10,10):
     value = zeroCheck(i)
     if value == 0:
     print("when x = %d , value of y become 0" %(i))
     break
     else:
     continue
