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
        book_columns = ('id', 'name', 'publisher_name', 'author_name', 'category_name', 'position_name', 'published_year', 'total_amount', 'available_amount', 'price')
        book_column_widths = [60, 160, 100, 100, 100, 100, 60, 60, 60, 60]
        book_labels = ['Mã sách', 'Tên sách', 'NXB', 'Tác giả', 'Thể loại sách', 'Vị trí', 'Năm XB', 'SL tổng', 'SL tồn kho', 'Đơn giá']
        book_vars = []
        for i in range(len(book_labels)):
            book_vars.append(tk.StringVar())
        search_var = tk.StringVar()
        cb_index_arr = [2, 3, 4, 5]
        cb_object_names = ['publisher', 'author', 'category', 'position']
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
        label_arr = []
        entry_arr = []

        def cb_id_to_value(object_name, id):
            for i in range(len(id_list_arr[object_name])):
                if (id == id_list_arr[object_name][i]):
                    return value_list_arr[object_name][i]
            return ''

        def cb_value_to_id(object_name, value):
            for i in range(len(value_list_arr[object_name])):
                if (value == value_list_arr[object_name][i]):
                    return id_list_arr[object_name][i]
            return ''

        def parse_row(row):
            parsed_row = []
            for i in range(len(row)):
                if (not i in cb_index_arr):
                    parsed_row.append(row[i])
                else:
                    object_name = cb_object_names[i - 2]
                    parsed_row.append(cb_id_to_value(object_name, row[i]))
            return parsed_row

        def get_entry_values():
            values = []
            for i in range(len(book_vars)):
                if (not i in cb_index_arr):
                    values.append(book_vars[i].get())
                else:
                    object_name = cb_object_names[i - 2]
                    values.append(cb_value_to_id(object_name, book_vars[i].get()))
            return values

        def search():
            try:
                # Clear the treeview list items
                for item in tree.get_children():
                    tree.delete(item)
                search_value = search_var.get()
                result = get_element_list_by('book', 'name', search_value)
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

        def add():
            try:
                values = get_entry_values()
                result = append_element('book', values)
                if (result):
                    showinfo(title='Success', message='Thêm sách thành công!')
                    get_all()
                else:
                    showerror(title='Error', message='Thêm sách thất bại!')
            except Exception as e:
                print('add()', e)
            finally:
                pass

        def edit():
            try:
                values = values = get_entry_values()
                result = update_element('book', values)
                if (result):
                    showinfo(title='Success', message='Sửa sách thành công!')
                    get_all()
                else:
                    showerror(title='Error', message='Sửa sách thất bại!')
            except Exception as e:
                print('add()', e)
            finally:
                pass

        def delete():
            try:
                values = values = get_entry_values()
                result = delete_element_by_id('book', values[0])
                if (result):
                    showinfo(title='Success', message='Xóa sách thành công!')
                    get_all()
                else:
                    showerror(title='Error', message='Xóa sách thất bại!')
            except Exception as e:
                print('add()', e)
            finally:
                pass

        # Left menu
        menu_left = tk.Frame(self)
        menu_left.columnconfigure(0, weight=1)
        menu_left.rowconfigure(0, weight=0)
        menu_left.rowconfigure(1, weight=1)
        menu_left.rowconfigure(2, weight=0)

        menu_left.grid(column=0, row=0, sticky=tk.NSEW, padx=(10, 0), pady=10)

        # Upper left menu
        menu_upper_left = tk.Frame(menu_left, highlightbackground='#ababab', highlightthickness=1)
        menu_upper_left.columnconfigure(0, weight=2)
        menu_upper_left.columnconfigure(1, weight=1)
        menu_upper_left.rowconfigure(0, weight=1)
        
        menu_upper_left.grid(column=0, row=0, sticky=tk.NSEW)

        entry_search = ttk.Entry(menu_upper_left, textvariable=search_var)
        entry_search.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

        button_search = ttk.Button(menu_upper_left, text='Tìm tên sách', compound=tk.LEFT, command=lambda: search())
        button_search.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

        # Middle left menu
        menu_middle_left = tk.Frame(menu_left, highlightbackground='#ababab', highlightthickness=1)
        menu_middle_left.columnconfigure(0, weight=1)
        menu_middle_left.columnconfigure(1, weight=2)
        menu_middle_left.rowconfigure(10, weight=1)
        
        menu_middle_left.grid(column=0, row=1, sticky=tk.NSEW, pady=10)

        # Get combobox values
        def get_cb_values():
            try:
                for object_name in cb_object_names:
                    result = get_element_list(object_name)
                    if (not result or len(result) == 0):
                        showerror(title='Error', message='Không có dữ liệu.')
                    else:
                        for row in result:
                            id_list_arr[object_name].append(row[0])
                            value_list_arr[object_name].append(row[1])
            except Exception as e:
                print('get_cb_values()', e)
                pass

        # Populate label and entry arrays
        for i in range(len(book_labels)):
            label_arr.append(ttk.Label(menu_middle_left, text=book_labels[i]))
            label_arr[i].grid(column=0, row=i, sticky=tk.W, padx=10, pady=10)
            if (not i in cb_index_arr):
                entry_arr.append(ttk.Entry(menu_middle_left, textvariable=book_vars[i]))
            else:
                entry_arr.append(ttk.Combobox(menu_middle_left, textvariable=book_vars[i]))
                match i:
                    case 2:
                        entry_arr[i]['values'] = value_list_arr['publisher']
                    case 3:
                        entry_arr[i]['values'] = value_list_arr['author']
                    case 4:
                        entry_arr[i]['values'] = value_list_arr['category']
                    case 5:
                        entry_arr[i]['values'] = value_list_arr['position']
                entry_arr[i]['state'] = 'readonly'
            entry_arr[i].grid(column=1, row=i, sticky=tk.EW, padx=(0, 10), pady=10)

        # Lower left menu
        menu_lower_left = tk.Frame(menu_left, highlightbackground='#ababab', highlightthickness=1)
        menu_lower_left.columnconfigure(0, weight=1)
        menu_lower_left.columnconfigure(1, weight=1)
        menu_lower_left.columnconfigure(2, weight=1)
        menu_lower_left.rowconfigure(0, weight=1)

        menu_lower_left.grid(column=0, row=2, sticky=tk.NSEW)

        button_add = ttk.Button(menu_lower_left, text='Thêm', compound=tk.LEFT, command=lambda: add())
        button_add.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

        button_edit = ttk.Button(menu_lower_left, text='Sửa', compound=tk.LEFT, command=lambda: edit())
        button_edit.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

        button_delete = ttk.Button(menu_lower_left, text='Xóa', compound=tk.LEFT, command=lambda: delete())
        button_delete.grid(column=2, row=0, sticky=tk.NSEW, padx=10, pady=10)

        # Right menu
        menu_right = tk.Frame(self, highlightbackground='#ababab', highlightthickness=1)
        menu_right.columnconfigure(0, weight=1)
        menu_right.columnconfigure(1, weight=0)
        menu_right.rowconfigure(0, weight=1)

        menu_right.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

        tree = ttk.Treeview(menu_right, columns=book_columns, show='headings')

        # Define headings
        for i in range(len(book_columns)):
            tree.heading(book_columns[i], text=book_labels[i])

        # Customize columns
        for i in range(len(book_columns)):
            tree.column(book_columns[i], width=book_column_widths[i], anchor=tk.W)

        def update_entry_values(record):
            for i in range(len(book_vars)):
                book_vars[i].set(record[i])

        def item_selected(event):
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                record = item['values']
                update_entry_values(record)

        # Selection event
        tree.bind('<<TreeviewSelect>>', item_selected)

        tree.grid(row=0, column=0, sticky=tk.NSEW)

        scrollbar = ttk.Scrollbar(menu_right, orient='vertical', command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(column=1, row=0, sticky=tk.NS)

        # Populate data
        def get_all():
            try:
                # Clear the treeview list items
                for item in tree.get_children():
                    tree.delete(item)

                result = get_element_list('book')
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

        # API calling functions
        get_cb_values()
        get_all()