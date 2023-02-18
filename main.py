from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def generate_password():
    pw_entry.delete(0, END)  # deletes the previous generated password

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    pw_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SEARCH FOR PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("saved passwords.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="File Error", message="No data file found.")
    else:
        if website in data:
            dict_email = data[website]["email"]
            dict_password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email/Usermame: {dict_email}\nPassword: {dict_password}")
        else:
            messagebox.showerror(title="Website Error", message=f"No details for {website} website exists.")

# ----------------------------- SOLUTION 2 --------------------------------------- #
# Catch the website not found error with a KeyError exception. KEEP IN MIND! IF WE CAN MAKE EASY USE OF IF/ELSE STATEMENTS
# THEN WE SHOULD AVOID USING EXCEPTIONS BECAUSE THEIR USE IS ONLY FOR OCCASIONS WHERE AN ERROR CAN'T BE DEALT WITH ANOTHER WAY!

# except KeyError as website:\
#    messagebox.showerror(title="Website Error", message=f"No details for {website} website exists.")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_user_entry.get()
    password = pw_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="Error", message="Please don't leave any fields empty!")
    else:
        try:  # try to read from the file
            with open("saved passwords.json", "r") as data_file:
                data = json.load(data_file)  # read from a json formatted file (use "r" in open() func)
        except (FileNotFoundError, json.decoder.JSONDecodeError):  # if the file doesn't exist, we create it
            with open("saved passwords.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)  # write to a json formatted file (use "w" in open() func)
        else:  # if the file exists and is read, we update it with the new_data and then write the updated data to
            # the data_file
            data.update(new_data)  # add new data to an already existing file (use "r" in open() func)
            with open("saved passwords.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            pw_entry.delete(0, END)
            messagebox.showinfo(title="Confirmation", message="Password saved!")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)
# ----------------------------- LABELS ----------------------------- #
# Website label
website_label = Label(text="Website:", font=("Arial", 12), padx=5, pady=5)
website_label.grid(column=0, row=1)

# Email/Username label
email_user_label = Label(text="Email/Username:", font=("Arial", 12), padx=5, pady=5)
email_user_label.grid(column=0, row=2)

# Password label
pw_label = Label(text="Password:", font=("Arial", 12), padx=5, pady=5)
pw_label.grid(column=0, row=3)

# ----------------------------- ENTRIES ----------------------------- #
# Website entry
website_entry = Entry(width=33)
website_entry.grid(column=1, row=1)
website_entry.focus()

# Email/Username entry
email_user_entry = Entry(width=52)
email_user_entry.grid(column=1, row=2, columnspan=2)
email_user_entry.insert(0, "lefos12@hotmail.com")

# Password entry
pw_entry = Entry(width=33)
pw_entry.grid(column=1, row=3)

# ----------------------------- BUTTONS ----------------------------- #
# Generate Password button
generate_pw_button = Button(text="Generate Password", command=generate_password)
generate_pw_button.grid(column=2, row=3)

# Add button
add_button = Button(text="Add", width=44, command=save)
add_button.grid(column=1, row=4, columnspan=2)

# Search button
search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
