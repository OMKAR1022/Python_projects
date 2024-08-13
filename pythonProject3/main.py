import pickle
import pyperclip

user_id = input("Enter your user id (Press 1 to create account) :")

dictionary ={}

#with open("Myproject||pass.txt","br") as filewrite:
    #dictionary = pickle.load(filewrite)

if "1" in user_id:
    email = input("Enter your user id :")

    with open("Myproject||email.txt", "w") as f:
        f.write(email)

    password = input ("Enter your password :")

    with open("Myproject||pass.txt","w") as a:
       a.write(password)

with open("Myproject||email.txt","r") as fr:
    store_email = fr.read()

if user_id == store_email:
    password2= input("Enter a password : " )
    with open("Myproject||pass.txt","r") as ar:
        store_pass= ar.read()

    if password2 == store_pass:
        conf = input("to know your password '1' to save your password press '2' : ")

        if "2" in conf:
            account = input("Enter your account name")
            acc_pass = input("Enter your password")

            confirmation = input("Would you like to save it(y/n)")

            if "y" in confirmation:
                dictionary[account] = acc_pass

                with open("Myproject||pass.txt" , "bw") as readfile:
                    dictionary = pickle.dump(dictionary, readfile ,protocol=2)

                print(f"Done ! your {account}'s password has been saved")

            else:
                print("Your Data has not saved...")

        if "1" in conf:
            email1= input("Which account's password you want to know :")

            with open("Myproject||pass.txt" , "br")as file:
                dictionary = pickle.load(file)

            if email1 in dictionary:
                print(f"your {email}'s password is {dictionary[email1]}")
                print("your password has been saved to your clipboard")
                pyperclip.copy(dictionary[email1])

            else:
                print("This password is not saved")
