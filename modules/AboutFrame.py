import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
from apis.googlesheetsapi import *

class AboutFrame(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text='Author: Nguyễn Kim Cương')
        label.pack(ipadx=10, ipady=10)