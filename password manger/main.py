from tkinter import *
from tkinter.messagebox import showinfo
from cryptography.fernet import Fernet
import os

root = Tk()
root.title("omkar password manger")
# root.geometry("500*300")

websiteVar = StringVar()
passwordVar = StringVar()
emailVar = StringVar()
totalPasswords = StringVar()

if os.path.isfile("encrypt.txt"):
    with open("encrypt.txt", 'r') as file:
        data = file.readlines()

    totalPasswords.set(f"Total Passwords: {len(data)}")
else:
    totalPasswords.set("Total Passwords: 0")


def generate_key():
    with open("mode.txt", "r") as file:
        data = file.read()
        print(data)
    if data == "0":
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

    with open("mode.txt", "w") as file:
        file.write("1")

    root.config(menu=mainMenu)


def load_key():
    return open("secret.key", "rb").read()


def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message


def exportAllPasswords():
    key = load_key()
    f = Fernet(key)
    with open("encrypt.txt", "r") as file:
        enc = file.readlines()
    for index, data in enumerate(enc):
        ency = bytes(data, 'utf-8')
        decrypted_message = f.decrypt(ency)
        print(decrypted_message.decode())
        with open("decrypt.txt", "a") as file:
            file.write(decrypted_message.decode())
            file.write("\n")




def savePassword():
    email = emailVar.get()
    password = passwordVar.get()
    website = websiteVar.get()
    string = f'{website} {email} {password}'
    message = encrypt_message(string)
    print(message)
    with open("encrypt.txt", "w") as file:
        file.write(message.decode("utf-8"))
        file.write("\n")


def showAllPasswords():
    pass

def aboutSoftware():
    showinfo("About", "Software: Omkar password Manger \n version:")


softwareLabel = Label(root, text="Omkar Password Manager", font=("Calibri", 30))
softwareLabel.pack()
websiteLabel = Label(root, text="Website Name:")
websiteLabel.pack()

websiteEntry = Entry(root, textvariable=websiteVar)
websiteEntry.pack()

emailLabel = Label(root, text="Email/Username:")
emailLabel.pack()

emailEntry = Entry(root, textvariable=emailVar)
emailEntry.pack()

passwordLabel = Label(root, text="Password:")
passwordLabel.pack()

passwordEntry = Entry(root, textvariable=passwordVar, show="●")
passwordEntry.pack()

saveBtn = Button(root, text="Save My Password", command=savePassword,)
saveBtn.pack()

actionLabel = Label(root, text="ACTIONS", font=("Calibri", 25))
actionLabel.pack()

actionBtnFrame = Frame(root)
actionBtnFrame.pack()

showPasswordBtn = Button(actionBtnFrame, text="Show All Passwords", command=showAllPasswords)
showPasswordBtn.pack(side=LEFT, padx=10)

exportPasswordBtn = Button(actionBtnFrame, text="Export All Passwords", command=exportAllPasswords)
exportPasswordBtn.pack(side=LEFT)

mainMenu = Menu(root)
optionsMenu = Menu(mainMenu, tearoff=0)
optionsMenu.add_command(label="Show All Passwords", command=showAllPasswords)
optionsMenu.add_command(label="Export All Passwords", command=exportAllPasswords)
optionsMenu.add_separator()
optionsMenu.add_command(label="Exit", command=root.destroy)
mainMenu.add_cascade(menu=optionsMenu, label="Options")
aboutMenu = Menu(mainMenu, tearoff=0)
aboutMenu.add_command(label="About Software", command=aboutSoftware)
mainMenu.add_cascade(menu=aboutMenu, label="About")
root.config(menu=mainMenu)
root.mainloop()
