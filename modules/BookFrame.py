import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
from apis.google_sheets_api import *

class BookFrame(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        # Configure frame
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)

        # Variables
        book_headings = controller.book_headings
        book_labels = controller.book_labels
        book_vars = controller.book_vars

        # Left menu
        menu_left = tk.Frame(self, highlightbackground='#ababab', highlightthickness=1)
        menu_left.columnconfigure(0, weight=1)
        menu_left.rowconfigure(0, weight=1)
        menu_left.rowconfigure(1, weight=0)

        menu_left.grid(column=0, row=0, sticky=tk.NSEW, padx=(10, 0), pady=10)

        # Upper left menu
        menu_upper_left = tk.Frame(menu_left)
        menu_upper_left.columnconfigure(0, weight=1)
        menu_upper_left.columnconfigure(1, weight=2)
        menu_upper_left.rowconfigure(10, weight=1)
        
        menu_upper_left.grid(column=0, row=0, sticky=tk.NSEW)

        label_arr = []
        entry_arr = []
        for i in range(len(book_labels)):
            label_arr.append(ttk.Label(menu_upper_left, text=book_labels[i]))
            label_arr[i].grid(column=0, row=i, sticky=tk.W, padx=10, pady=10)
            entry_arr.append(ttk.Entry(menu_upper_left, textvariable=book_vars[i]))
            entry_arr[i].grid(column=1, row=i, sticky=tk.EW, padx=(0, 10), pady=10)

        # Lower left menu
        menu_lower_left = tk.Frame(menu_left)
        menu_lower_left.columnconfigure(0, weight=1)
        menu_lower_left.columnconfigure(1, weight=1)
        menu_lower_left.rowconfigure(0, weight=1)
        menu_lower_left.rowconfigure(1, weight=1)

        menu_lower_left.grid(column=0, row=1, sticky=tk.NSEW)

        def search():
            try:
                # Clear the treeview list items
                for item in tree.get_children():
                    tree.delete(item)

                searchValue = book_vars[1].get()
                result = get_objects_by_name('book', searchValue)
                if (not result or len(result) == 0):
                    showerror(title='Error', message='Không có dữ liệu.')
                else:
                    rows = []
                    for row in result:
                        rows.append(tuple(row))
                    for row in rows:
                        tree.insert('', tk.END, values=row)
            except Exception as e:
                print(e)
                pass
            # finally:
            #     book_vars[1].delete(0, 'end')

        button_search = ttk.Button(menu_lower_left, text='Tìm', compound=tk.LEFT, command=lambda: search())
        button_search.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

        def add():
            print()

        button_add = ttk.Button(menu_lower_left, text='Thêm', compound=tk.LEFT, command=lambda: add())
        button_add.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

        def edit():
            print()

        button_edit = ttk.Button(menu_lower_left, text='Sửa', compound=tk.LEFT, command=lambda: edit())
        button_edit.grid(column=0, row=1, sticky=tk.NSEW, padx=10, pady=10)

        def delete():
            print()

        button_delete = ttk.Button(menu_lower_left, text='Xóa', compound=tk.LEFT, command=lambda: delete())
        button_delete.grid(column=1, row=1, sticky=tk.NSEW, padx=10, pady=10)

        # Right menu
        menu_right = tk.Frame(self, highlightbackground='#ababab', highlightthickness=1)
        menu_right.columnconfigure(0, weight=1)
        menu_right.columnconfigure(1, weight=0)
        menu_right.rowconfigure(0, weight=1)

        menu_right.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

        # Define columns
        columns = book_headings

        tree = ttk.Treeview(menu_right, columns=columns, show='headings')

        # Define headings
        for i in range(len(columns)):
            tree.heading(columns[i], text=book_labels[i])

        widths = [20, 160, 30, 30, 30, 30, 30, 30, 30, 30]

        # Customize columns
        for i in range(len(columns)):
            tree.column(columns[i], width=widths[i], anchor=tk.W)

        def get_all():
            # Sample data
            # rows = []
            # for n in range(1, 100):
            #     rows.append((f'{n}', f'{n}', f'{n}', f'{n}', f'{n}', f'{n}', f'{n}', f'{n}', f'{n}', f'{n}'))
            # for row in rows:
            #     tree.insert('', tk.END, values=row)
            try:
                # Clear the treeview list items
                for item in tree.get_children():
                    tree.delete(item)

                result = get_objects('book')
                if (not result or len(result) == 0):
                    showerror(title='Error', message='Không có dữ liệu.')
                else:
                    rows = []
                    for row in result:
                        rows.append(tuple(row))
                    for row in rows:
                        tree.insert('', tk.END, values=row)
            except Exception as e:
                print(e)
                pass

        # Initialize data
        get_all()

        def item_selected(event):
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                record = item['values']
                # Show a message
                showinfo(title='Information', message=record)

        # Selection event
        tree.bind('<<TreeviewSelect>>', item_selected)

        tree.grid(row=0, column=0, sticky=tk.NSEW)

        scrollbar = ttk.Scrollbar(menu_right, orient='vertical', command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(column=1, row=0, sticky=tk.NS)