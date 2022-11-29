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
        book_headings = ('id', 'name', 'publisher_name', 'author_name', 'category_name', 'position_name', 'published_year', 'total_amount', 'available_amount', 'price')
        book_labels = ['Mã sách', 'Tên sách', 'NXB', 'Tác giả', 'Thể loại sách', 'Vị trí', 'Năm XB', 'SL tổng', 'SL tồn kho', 'Đơn giá']
        book_vars = []
        for i in range(len(book_labels)):
            book_vars.append(tk.StringVar())
        label_arr = []
        entry_arr = []
        cb_index_arr = [2, 3, 4, 5]
        cb_value_arr = []
        object_names = ['publisher', 'author', 'category', 'position']
        id_list_arr = {
            'publisher': [],
            'author': [],
            'category': [],
            'position': []
        }
        value_list_arr = {
            'publisher': [],
            'author': [],
            'category': [],
            'position': []
        }

        # Get combobox values
        def get_cb_values():
            try:
                for object_name in object_names:
                    result = get_objects(object_name)
                    if (not result or len(result) == 0):
                        showerror(title='Error', message='Không có dữ liệu.')
                    else:
                        for row in result:
                            id_list_arr[object_name].append(row[0])
                            value_list_arr[object_name].append(row[1])
            except Exception as e:
                print('get_cb_values()', e)
                pass

        def id_to_value(object_name, id):
            for i in range(len(id_list_arr[object_name])):
                if (id == id_list_arr[object_name][i]):
                    return value_list_arr[object_name][i]
            return ''

        def parse_row(row):
            parsed_row = []
            for i in range(len(row)):
                if (not i in cb_index_arr):
                    parsed_row.append(row[i])
                else:
                    object_name = object_names[i - 2]
                    parsed_row.append(id_to_value(object_name, row[i]))
            return parsed_row

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
                        parsed_row = parse_row(row)
                        rows.append(tuple(parsed_row))
                    for row in rows:
                        tree.insert('', tk.END, values=row)
            except Exception as e:
                print('search()', e)
                pass
            # finally:
            #     book_vars[1].delete(0, 'end')

        def add():
            print('add')

        def edit():
            print('edit')

        def delete():
            print('delete')

        # Left menu
        menu_left = tk.Frame(self)
        menu_left.columnconfigure(0, weight=1)
        menu_left.rowconfigure(0, weight=0)
        menu_left.rowconfigure(1, weight=0)
        menu_left.rowconfigure(2, weight=1)

        menu_left.grid(column=0, row=0, sticky=tk.NSEW, padx=(10, 0), pady=10)

        # Upper left menu
        menu_upper_left = tk.Frame(menu_left, highlightbackground='#ababab', highlightthickness=1)
        menu_upper_left.columnconfigure(0, weight=1)
        menu_upper_left.rowconfigure(0, weight=1)
        
        menu_upper_left.grid(column=0, row=0, sticky=tk.NSEW)

        button_search = ttk.Button(menu_upper_left, text='Tìm', compound=tk.LEFT, command=lambda: search())
        button_search.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

        # Middle left menu
        menu_middle_left = tk.Frame(menu_left, highlightbackground='#ababab', highlightthickness=1)
        menu_middle_left.columnconfigure(0, weight=1)
        menu_middle_left.columnconfigure(1, weight=1)
        menu_middle_left.columnconfigure(2, weight=1)
        menu_middle_left.rowconfigure(0, weight=1)

        menu_middle_left.grid(column=0, row=1, sticky=tk.NSEW, pady=10)

        button_add = ttk.Button(menu_middle_left, text='Thêm', compound=tk.LEFT, command=lambda: add())
        button_add.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

        button_edit = ttk.Button(menu_middle_left, text='Sửa', compound=tk.LEFT, command=lambda: edit())
        button_edit.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

        button_delete = ttk.Button(menu_middle_left, text='Xóa', compound=tk.LEFT, command=lambda: delete())
        button_delete.grid(column=2, row=0, sticky=tk.NSEW, padx=10, pady=10)

        # Lower left menu
        menu_lower_left = tk.Frame(menu_left, highlightbackground='#ababab', highlightthickness=1)
        menu_lower_left.columnconfigure(0, weight=1)
        menu_lower_left.columnconfigure(1, weight=2)
        menu_lower_left.rowconfigure(10, weight=1)
        
        menu_lower_left.grid(column=0, row=2, sticky=tk.NSEW)

        get_cb_values()

        # Populate label and entry arrays
        for i in range(len(book_labels)):
            label_arr.append(ttk.Label(menu_lower_left, text=book_labels[i]))
            label_arr[i].grid(column=0, row=i, sticky=tk.W, padx=10, pady=10)
            if (not i in cb_index_arr):
                entry_arr.append(ttk.Entry(menu_lower_left, textvariable=book_vars[i]))
            else:
                entry_arr.append(ttk.Combobox(menu_lower_left, textvariable=book_vars[i]))
                match i:
                    case 2:
                        entry_arr[i]['values'] = value_list_arr['publisher']
                    case 3:
                        entry_arr[i]['values'] = value_list_arr['author']
                    case 4:
                        entry_arr[i]['values'] = value_list_arr['category']
                    case 5:
                        entry_arr[i]['values'] = value_list_arr['position']
                    case _:
                        entry_arr[i]['values'] = []
                entry_arr[i]['values'] = []
                entry_arr[i]['state'] = 'readonly'
            entry_arr[i].grid(column=1, row=i, sticky=tk.EW, padx=(0, 10), pady=10)

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

        widths = [60, 160, 100, 100, 100, 100, 60, 60, 60, 60]

        # Customize columns
        for i in range(len(columns)):
            tree.column(columns[i], width=widths[i], anchor=tk.W)

        def get_books():
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
                        parsed_row = parse_row(row)
                        rows.append(tuple(parsed_row))
                    for row in rows:
                        tree.insert('', tk.END, values=row)
            except Exception as e:
                print('get_books()', e)
                pass

        # Populate data
        get_books()

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