#tuple -- data types
# []
# ()

words = ("spam", "eggs", "sausages")

print(words[0])
print(words[1])
print(words[2])


# words[1] = "cheese"

empty_tuple = ()
prit(empty_tuple)

person = ("Alices", 30, "Engineer")

#Tuple unpacking
name,age,profession = person

print(name, "s","profession is", profession,"and she is", age, "years old.")