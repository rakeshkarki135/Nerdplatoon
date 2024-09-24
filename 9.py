# 9, 10
fruit = ('banana', 'apple', 'orange','mango')
vegetables = ('tomato','onion','garlics','turnip')
animal = ('cow','dog','cat','rat')

food_stuff_tp = fruit + vegetables + animal

divider = len(food_stuff_tp)//2

middleitem = food_stuff_tp[divider]

tuple1 = food_stuff_tp[:divider]
tuple2 = food_stuff_tp[divider:]

print(middleitem)
print(tuple1)
print(tuple2)