from tkinter import * #Used for GUI elements like windows, labels, buttons, etc
from tkinter import messagebox #For showing popup messages (like errors or success)
from random import choice, randint, shuffle
import customtkinter as ctk #A modern, styled version of Tkinter with themes and rounded widgets.
import pyperclip #Allows copying passwords to clipboard.
import json #Used to save/load password data from a file.
  #looks structured data

# CONFIGURATION
MASTER_PASSWORD = "password"

#GLOBAL VARIABLES

main_window = None
website_entry = None
email_entry = None
password_entry = None


# MASTER PASSWORD SCREEN
def check_master_password():
    """Check master password is correct"""
    entered_password = master_entry.get()
    if not entered_password:
        messagebox.showerror("Error", "Please enter a password!")
        return

    if entered_password == MASTER_PASSWORD:
        login_window.destroy()
        open_main_app()
    else:
        messagebox.showerror("Access Denied", "Incorrect master password!")
        master_entry.delete(0, END)
        master_entry.focus()


def create_login_window():
    """Create and show the login window"""
    global login_window, master_entry

    login_window = ctk.CTk()
    login_window.title("Login - Password Manager")
    login_window.geometry("600x400")
    login_window.resizable(False, False)

    # Center the window
    login_window.eval('tk::PlaceWindow . center')

    # Main frame
    #A Frame is a container widget used to group other widgets together inside a window
    main_frame = ctk.CTkFrame(login_window)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Title
    title_label = ctk.CTkLabel(main_frame, text="Password Manager",
                               font=ctk.CTkFont(size=20, weight="bold"))
    title_label.pack(pady=(20, 10))

    # Instructions
    info_label = ctk.CTkLabel(main_frame, text="Enter Master Password:")
    info_label.pack(pady=5)

    # Password entry
    master_entry = ctk.CTkEntry(main_frame, show="*", width=250,
                                placeholder_text="Master Password")
    master_entry.pack(pady=10)
    master_entry.bind("<Return>", lambda e: check_master_password())
    #When the user presses the Enter key while typing in the
    # password box (master_entry), run the check_master_password() function —
    # just like clicking the Login button.

    # Login button
    login_btn = ctk.CTkButton(main_frame, text="Login",
                              command=check_master_password,
                              width=250)
    login_btn.pack(pady=10)

    # Focus on entry
    master_entry.focus()

    login_window.mainloop()


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(3, 5))]
    password_symbols = [choice(symbols) for _ in range(randint(1, 2))]
    password_numbers = [choice(numbers) for _ in range(randint(1, 2))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)  # Clear existing password first
    password_entry.insert(0, password)
    pyperclip.copy(password)


#SAVE PASSWORD
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {
        "email": email,
        "password": password,
    }}

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # reading
                data = json.load(data_file)
        except:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # update
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:  # Fixed typo: was "date_file"
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="File not found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(f"{website}", f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exist")


# ---------------------------- MAIN APP ------------------------------- #
def open_main_app():
    """Create and show the main password manager window"""
    global main_window, website_entry, email_entry, password_entry

    main_window = ctk.CTk()
    main_window.title("Password Manager - MyPass")
    main_window.geometry("600x500")
    main_window.resizable(False, False)
    main_window.eval('tk::PlaceWindow . center')

    main_frame = ctk.CTkFrame(main_window)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Title
    title_label = ctk.CTkLabel(main_frame, text="Password Manager",
                               font=ctk.CTkFont(size=24, weight="bold"))
    title_label.pack(pady=(20, 30))

    # Input frame
    input_frame = ctk.CTkFrame(main_frame)
    input_frame.pack(fill="x", padx=20, pady=10)

    # Website
    ctk.CTkLabel(input_frame, text="Website:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    website_entry = ctk.CTkEntry(input_frame, width=200, placeholder_text="e.g., gmail.com")
    website_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # Search button
    search_btn = ctk.CTkButton(input_frame, text="Search", command=find_password, width=100)
    search_btn.grid(row=0, column=2, padx=10, pady=10)

    # Email/Username
    ctk.CTkLabel(input_frame, text="Email/Username:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    email_entry = ctk.CTkEntry(input_frame, width=200, placeholder_text="your@email.com")
    email_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # Password
    ctk.CTkLabel(input_frame, text="Password:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    password_entry = ctk.CTkEntry(input_frame, width=200, placeholder_text="Generated password")
    password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # Generate password button
    generate_btn = ctk.CTkButton(input_frame, text="Generate", command=generate_password, width=100)
    generate_btn.grid(row=2, column=2, padx=10, pady=10)

    add_button = ctk.CTkButton(input_frame, text="Add", width=250, command=save)
    add_button.grid(row=4, column=1, columnspan=2, pady=5)

    main_window.mainloop()


# ---------------------------- MAIN EXECUTION ------------------------------- #
if __name__ == "__main__":
    # Set appearance
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    # Start with login window
    create_login_window()