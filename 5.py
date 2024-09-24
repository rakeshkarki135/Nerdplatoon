sentence = "I am a teacher and i love to inspire and teach"

words = sentence.split(' ')
unique_words = []

for i in words:
     count = words.count(i)
     if count == 1:
     unique_words.append(i)
     else:
     continue

print(unique_words)