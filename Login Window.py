import tkinter as tk
import mysql.connector
from tkinter import messagebox
import subprocess

class loginForm:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")

        # Center the window on the screen
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws - 400) / 2  # Set your desired width
        y = (hs - 300) / 2  # Set your desired height
        self.master.geometry('%dx%d+%d+%d' % (400, 300, x, y))

        # Create a main frame with the background color
        self.frame = tk.Frame(self.master, bg='#2d3032')
        self.frame.pack(fill='both', expand=True)

        # Create labels and text entry widgets with the same background color

        self.LoginLabel = tk.Label(self.frame, text='Login', bg='#2d3032',
                                      font=('Helvetica', 20), fg='white')
        self.LoginLabel.pack(pady=(0, 10))

        self.usernameLabel = tk.Label(self.frame, text='Username:', bg='#2d3032',
                                      font=('Helvetica', 12), fg='white')
        self.usernameLabel.pack()
        self.usernameTextbox = tk.Entry(self.frame, font=('Helvetica', 12), width=25,
                                        borderwidth='2', relief='ridge')
        self.usernameTextbox.pack(pady=(0, 10))

        self.passwordLabel = tk.Label(self.frame, text='Password:', bg='#2d3032',
                                      font=('Helvetica', 12), fg='white')
        self.passwordLabel.pack()
        self.passwordTextbox = tk.Entry(self.frame, show='*', font=('Helvetica', 12),
                                        width=25, borderwidth='2', relief='ridge')
        self.passwordTextbox.pack(pady=(0, 10))

        # Create login and cancel buttons side by side with the same background color
        self.btnsFrame = tk.Frame(self.frame, bg='#2d3032')
        self.btnsFrame.pack()

        self.btnLogin = tk.Button(self.btnsFrame, text='Login', bg='light grey',
                                  font=('Helvetica', 12), fg='black', padx=25,
                                  pady=5, command=self.login_func)
        self.btnLogin.pack(side='left', padx=(10, 20), pady="20")

        self.btnCancel = tk.Button(self.btnsFrame, text='Cancel', bg='light grey',
                                   font=('Helvetica', 12), fg='black', padx=25,
                                   pady=5, command=self.close_window)
        self.btnCancel.pack(side='left', padx=(20, 10), pady="20")

    def login_func(self):
        username = self.usernameTextbox.get()
        password = self.passwordTextbox.get()

        # Establish a connection to the MySQL database
        db = mysql.connector.connect(
            host='localhost',
            port='3307',
            user='root',
            password='root',
            database='resultsystem'
        )

        cursor = db.cursor()

        select_query = 'SELECT * FROM login_data WHERE username = %s and password = %s'
        vals = (username, password,)

        cursor.execute(select_query, vals)
        user = cursor.fetchone()

        if user is not None:
            self.master.destroy()
            subprocess.run(["python", "Admin_page.py"])
        else:
            messagebox.showwarning('Error', 'Enter a Valid Username & Password')

        cursor.close()
        db.close()

    def close_window(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    app = loginForm(root)
    root.mainloop()

if __name__ == '__main__':
    main()
