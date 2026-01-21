class Person:
    # name = "Deepansh "
    occupation = "Founder" 
    networth = "More than you can afford pal"

    def __init__(self , full_name):
        # pass
        print("This is the constructor and it automatically runs when the object is created ")
        self.name = full_name

    def info(self):
        print(f"name of this person is {self.name} and he is a {self.occupation}")


a = Person("Shubham")
# print("I Have created object a ")
b = Person("Nikita")
# print("I Have created object b ")

print(f"The name of object a is {a.name} and the name of object b is {b.name}")

# a.name = "Shubham"
# a.occupation = "CA"

# b.name = "Nikita"
# b.occupation = "HR"

# a.info()
# b.info()


