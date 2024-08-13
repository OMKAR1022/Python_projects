# 2213411, JITEN MAHESHWARI .

# Create a hash table and handle the collision using linear probing with or without replacement .

# LINEAR PROBING (WITHOUT REPLACEMENT

list1=[]
j=1
y=int(input("Enter the array size:"))

for i in range(y):
    list1.append(0)
print("Initial array is:",list1)

for k in range (y):
    x=int(input("Enter the value:"))
    h=x%y
    z=h
    if list1[h]==0:
        list1[h]=x
        print(list1)
    else:
        while (list1[h]!=0):
            h=(h+j)%y
        list1[h]=x
        print(list1)
