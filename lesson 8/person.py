class Person:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"Hello, I am {self,name}, and I am {self.age}years old.")

personi1 = Person("Alice",15)
personi2 = Person("Bob", 17)

personi1.greet()
personi2.greet()