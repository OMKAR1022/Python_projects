print("Accesing a non existant index statement ")
list1=[1,2,3,'animus']
try:
    print("The seventh value is : ", list1[6])
except IndexError:
    print("The index is out of range")
