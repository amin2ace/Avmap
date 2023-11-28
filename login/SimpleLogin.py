"""Simple Login inerface with database
   GUI: code with tkinter module
   Database: sqlite3
   Main: None
   author: amin2ace
   email:avmap.py@gmail.com

    Returns:
        gui : this class has two main sign_in and sighn_up interface with store
        in a default relative path database (sqlite3).
        class simply instansiated by gui screen name passed as argument in string.
        if database is not found in same path of login.py then rebuild it.
    """
from tkinter.font import Font
import tkinter as tk
import sqlite3
from os import getcwd, path
from datetime import datetime



class Gui(tk.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__('Login Page', baseName, className, useTk, sync, use)
        hide_show = tk.PhotoImage(file='./hide_button.png')
        logo_icon = tk.PhotoImage(file='./icon.png')
        image = hide_show.subsample(7,7)
        self.iconphoto(True, logo_icon)
        self.title(screenName)
        self.geometry(f'500x245+{self.winfo_screenwidth()//2-250}+{self.winfo_screenheight()//2-245}')
        self.resizable(False, False)
        pane_1: tk.PanedWindow = tk.PanedWindow(self, orient='horizontal', borderwidth=1, height=100, width= 200)
        pane_2: tk.PanedWindow = tk.PanedWindow(self, orient='horizontal', borderwidth=1, height=100, width= 200)
        pane_3: tk.PanedWindow = tk.PanedWindow(self, orient='horizontal', borderwidth=1, height=100, width= 200)
        pane_1.pack(anchor='n')
        pane_2.pack(anchor='center')
        pane_3.pack(anchor='s')
        error_font = Font(family='Calibri', slant='italic', size=18, underline=True)
        
        def sign_up():
            if self.sign_up__btn['text'] == 'Sign in':
                self.signin_frame['text'] = 'Sign in...'
                self.sign_up__btn['text'] = 'Sign up'
            else:
                self.signin_frame['text'] = 'Sign up...'
                self.sign_up__btn['text'] = 'Sign in'
                
        def enter():
            username = self.username_ent.get()
            password = self.password_ent.get()
            user = User(username, password)
            if self.signin_frame['text'] == 'Sign in...': # sign in
                if user.check():
                    # self.check_label_['font'] = error_font
                    self.check_label_['fg'] = 'green'
                    self.check_label_['text'] = 'Logged in'
                else:
                    self.check_label_['font'] = error_font
                    self.check_label_['fg'] = 'red'
                    self.check_label_['text'] = 'username or password incorrect!'
            else: # sign up
                try:
                    assert user.add()
                except:
                    self.check_label_['font'] = error_font
                    self.check_label_['fg'] = 'red'
                    self.check_label_['text'] = 'Username Exists. try sign in instead'
                else:
                    self.check_label_['fg'] = 'blue'
                    self.check_label_['text'] = 'Successfuly Signed up'

        def show(sh):
            if sh == '*':
                self.password_ent['show'] = ''
            else:
                self.password_ent['show'] = '*'
                
        self.signin_frame: tk.Frame = tk.LabelFrame(pane_2, text='Sign in...', width=60,height=50, font='Calibri 25', padx=10, pady=10)                
        self.check_label_: tk.Label = tk.Label(pane_1, text='Enter username and password',font='Calibri 18', justify='center', pady=8)
        self.username_lbl: tk.Label = tk.Label(self.signin_frame, text='User name:', font='Arial 10', padx=10, pady=10)
        self.password_lbl: tk.Label = tk.Label(self.signin_frame, text='Password: ', font='Arial 10', padx=10, pady=10)
        self.spacer_e_lbl: tk.Label = tk.Label(self.signin_frame, width=2)
        self.username_ent: tk.Entry = tk.Entry(self.signin_frame, width=30, borderwidth=5, font="simsun 16")
        self.password_ent: tk.Entry = tk.Entry(self.signin_frame, width=30, borderwidth=5, font="simsun 16", show='*')
        self.enteranc_btn: tk.Button = tk.Button(self.signin_frame, text='Ckeck', width=6, padx=10, pady=10, command=enter)
        self.show_hid_btn: tk.Button = tk.Button(self.signin_frame, image=image, borderwidth=0, width=11, height=11,padx=20, command=lambda: show(self.password_ent['show']))
        self.sign_up__btn: tk.Button = tk.Button(self.signin_frame, text='Sign up', relief='flat', fg='blue', command=sign_up)
        
        ### Griding
        self.signin_frame.grid(column=0, row=0)
        self.check_label_.grid(column=0, row=0)
        self.username_lbl.grid(column=0, row=0)
        self.password_lbl.grid(column=0, row=1)
        self.spacer_e_lbl.grid(column=1, row=0, rowspan=2)
        self.username_ent.grid(column=2, row=0)
        self.password_ent.grid(column=2, row=1)
        self.enteranc_btn.grid(column=2, row=2, sticky='E')
        self.show_hid_btn.grid(column=3, row=1)
        self.sign_up__btn.grid(column=2, row=2, sticky='W')
          
        self.mainloop()


class User():
    def __init__(self, username: str, password: str) -> None:
        self.username: str = username
        self.password: str = password
        self.db_path = getcwd()
        self.data_base = sqlite3.connect(path.join(self.db_path, 'User_Accounts.db'))
        self.curser = self.data_base.cursor()
        self.curser.execute("CREATE TABLE IF NOT EXISTS USER_PASS (Time_stamp INT UNIQUE ,user_name TEXT UNIQUE, password TEXT)")
        self.data_base.commit()
        # if not self.check(): self.add()
        
    def add(self):
        try:
            with sqlite3.connect(path.join(self.db_path, 'User_Accounts.db')) as db:
                curser = db.cursor()
                curser.execute(f"INSERT INTO USER_PASS VALUES('{datetime.now().timestamp()}','{self.username}','{self.password}')")
                db.commit()
        except: return 0
        else: return 1
                
    def check(self):
        with sqlite3.connect(path.join(self.db_path, 'User_Accounts.db')) as db:
            curser = db.cursor()
            query_ = curser.execute(f"SELECT * FROM USER_PASS WHERE user_name='{self.username}' and password='{self.password}'")
            userpass = query_.fetchone()
            return userpass
