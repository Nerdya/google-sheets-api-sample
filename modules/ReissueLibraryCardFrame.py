import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
from apis.google_sheets_api import *

class ReissueLibraryCardFrame(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text='ReissueLCFrame')
        label.pack(ipadx=10, ipady=10)

    def call_apis(self):
        print('call_apis()')
