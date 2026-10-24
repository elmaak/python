#Error handling

#Try and except block

try:
    result = 10/10
except ZeroDivisionError:
    print("Oops!Tried to divide by zero")

#######
#key/value

fruits = {
    "apple" : 5,
    "banana" : 7,
    "orange" : 3
}

try:
    print(fruits["cherry"])
except KeyError:
    print("The key does not exst in the directory")


#BaseException

text = "This is not a number"

try: text_to_int = int(text)
except Exception as e :
    print("an error occurred while parsing data", e)

#else block
try:
    result = 10/2
except ZeroDivisionError:
    print("Division by zero occurred")
else:
    print("Division successful.Result:", result)

def divide_number(a,b):
    try:
        result = a/b
        print("Result of division",result)
    except ZeroDivisionError:
        print("Division of zero occurred")
    except TypeError:
        print("Invalid type for division")
    except Exception as e:
        print(f"Unexpected error: {e}")

divide_number(a:10,b:2)
divide_number(a:10,b:2)

