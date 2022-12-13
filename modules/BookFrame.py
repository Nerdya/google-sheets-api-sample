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
        self.frame_code = 'book'
        self.frame_name = 'sách'
        self.columns = ('id', 'name', 'publisher_name', 'author_name', 'category_name', 'position_name', 'published_year', 'total_amount', 'available_amount', 'price')
        self.column_widths = [60, 160, 100, 100, 100, 100, 60, 60, 60, 60]    # 860
        self.labels = ['Mã sách', 'Tên sách', 'NXB', 'Tác giả', 'Thể loại sách', 'Vị trí', 'Năm XB', 'SL tổng', 'SL tồn kho', 'Đơn giá']
        self.vars = []
        for i in range(len(self.labels)):
            self.vars.append(tk.StringVar())
        self.search_var = tk.StringVar()
        self.label_arr = []
        self.entry_arr = []

        # Combobox variables
        self.cb_index_arr = [2, 3, 4, 5]
        self.cb_object_names = ['publisher', 'author', 'category', 'position']
        self.id_list_arr = {
            'publisher': [],
            'author': [],
            'category': [],
            'position': []
        }
        self.value_list_arr = {
            'publisher': [],
            'author': [],
            'category': [],
            'position': []
        }

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

        entry_search = ttk.Entry(menu_upper_left, textvariable=self.search_var)
        entry_search.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

        button_search = ttk.Button(menu_upper_left, text='Tìm tên ' + self.frame_name, compound=tk.LEFT, command=lambda: self.search())
        button_search.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

        # Middle left menu
        menu_middle_left = tk.Frame(menu_left, highlightbackground='#ababab', highlightthickness=1)
        menu_middle_left.columnconfigure(0, weight=1)
        menu_middle_left.columnconfigure(1, weight=2)
        menu_middle_left.rowconfigure(10, weight=1)
        
        menu_middle_left.grid(column=0, row=1, sticky=tk.NSEW, pady=10)

        # Populate label and entry arrays
        for i in range(len(self.labels)):
            self.label_arr.append(ttk.Label(menu_middle_left, text=self.labels[i]))
            self.label_arr[i].grid(column=0, row=i, sticky=tk.W, padx=10, pady=10)
            if (not i in self.cb_index_arr):
                self.entry_arr.append(ttk.Entry(menu_middle_left, textvariable=self.vars[i]))
            else:
                self.entry_arr.append(ttk.Combobox(menu_middle_left, textvariable=self.vars[i]))
                match i:
                    case 2:
                        self.entry_arr[i]['values'] = self.value_list_arr['publisher']
                    case 3:
                        self.entry_arr[i]['values'] = self.value_list_arr['author']
                    case 4:
                        self.entry_arr[i]['values'] = self.value_list_arr['category']
                    case 5:
                        self.entry_arr[i]['values'] = self.value_list_arr['position']
                self.entry_arr[i]['state'] = 'readonly'
            self.entry_arr[i].grid(column=1, row=i, sticky=tk.EW, padx=(0, 10), pady=10)

        # Lower left menu
        menu_lower_left = tk.Frame(menu_left, highlightbackground='#ababab', highlightthickness=1)
        menu_lower_left.columnconfigure(0, weight=1)
        menu_lower_left.columnconfigure(1, weight=1)
        menu_lower_left.columnconfigure(2, weight=1)
        menu_lower_left.rowconfigure(0, weight=1)

        menu_lower_left.grid(column=0, row=2, sticky=tk.NSEW)

        button_add = ttk.Button(menu_lower_left, text='Thêm', compound=tk.LEFT, command=lambda: self.add())
        button_add.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

        button_edit = ttk.Button(menu_lower_left, text='Sửa', compound=tk.LEFT, command=lambda: self.edit())
        button_edit.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

        button_delete = ttk.Button(menu_lower_left, text='Xóa', compound=tk.LEFT, command=lambda: self.delete())
        button_delete.grid(column=2, row=0, sticky=tk.NSEW, padx=10, pady=10)

        # Right menu
        menu_right = tk.Frame(self, highlightbackground='#ababab', highlightthickness=1)
        menu_right.columnconfigure(0, weight=1)
        menu_right.columnconfigure(1, weight=0)
        menu_right.rowconfigure(0, weight=1)

        menu_right.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

        self.tree = ttk.Treeview(menu_right, columns=self.columns, show='headings')

        # Define headings
        for i in range(len(self.columns)):
            self.tree.heading(self.columns[i], text=self.labels[i])

        # Customize columns
        for i in range(len(self.columns)):
            self.tree.column(self.columns[i], width=self.column_widths[i], anchor=tk.W)

        def update_entry_values(record):
            for i in range(len(self.vars)):
                self.vars[i].set(record[i])

        def item_selected(event):
            for selected_item in self.tree.selection():
                item = self.tree.item(selected_item)
                record = item['values']
                update_entry_values(record)

        # Selection event
        self.tree.bind('<<TreeviewSelect>>', item_selected)

        self.tree.grid(row=0, column=0, sticky=tk.NSEW)

        scrollbar = ttk.Scrollbar(menu_right, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(column=1, row=0, sticky=tk.NS)

    def cb_id_to_value(self, object_name, id):
        for i in range(len(self.id_list_arr[object_name])):
            if (id == self.id_list_arr[object_name][i]):
                return self.value_list_arr[object_name][i]
        return ''

    def cb_value_to_id(self, object_name, value):
        for i in range(len(self.value_list_arr[object_name])):
            if (value == self.value_list_arr[object_name][i]):
                return self.id_list_arr[object_name][i]
        return ''

    def parse_row(self, row):
        parsed_row = []
        for i in range(len(row)):
            if (not i in self.cb_index_arr):
                parsed_row.append(row[i])
            else:
                object_name = self.cb_object_names[i - 2]
                parsed_row.append(self.cb_id_to_value(object_name, row[i]))
        return parsed_row

    def get_entry_values(self):
        values = []
        for i in range(len(self.vars)):
            if (not i in self.cb_index_arr):
                values.append(self.vars[i].get())
            else:
                object_name = self.cb_object_names[i - 2]
                values.append(self.cb_value_to_id(object_name, self.vars[i].get()))
        return values

    # Get combobox values
    def get_cb_values(self):
        try:
            for object_name in self.cb_object_names:
                result = get_element_list(object_name)
                if (not result or len(result) == 0):
                    showerror(title='Error', message='Không có dữ liệu.')
                else:
                    for row in result:
                        self.id_list_arr[object_name].append(row[0])
                        self.value_list_arr[object_name].append(row[1])
        except Exception as e:
            print('get_cb_values()', e)
            pass

    def search(self):
        try:
            # Clear the treeview list items
            for item in self.tree.get_children():
                self.tree.delete(item)
            search_value = self.search_var.get()
            result = get_element_list_by(self.frame_code, 'name', search_value)
            if (not result or len(result) == 0):
                showerror(title='Error', message='Không có dữ liệu.')
            else:
                rows = []
                for row in result:
                    parsed_row = self.parse_row(row)
                    rows.append(tuple(parsed_row))
                for row in rows:
                    self.tree.insert('', tk.END, values=row)
        except Exception as e:
            print('search()', e)
            pass

    def add(self):
        try:
            values = self.get_entry_values()
            result = append_element(self.frame_code, values)
            if (result):
                showinfo(title='Success', message='Thêm ' + self.frame_name + ' thành công!')
                self.get_all()
            else:
                showerror(title='Error', message='Thêm ' + self.frame_name + ' thất bại!')
        except Exception as e:
            print('add()', e)
        finally:
            pass

    def edit(self):
        try:
            values = values = self.get_entry_values()
            result = update_element(self.frame_code, values)
            if (result):
                showinfo(title='Success', message='Sửa ' + self.frame_name + ' thành công!')
                self.get_all()
            else:
                showerror(title='Error', message='Sửa ' + self.frame_name + ' thất bại!')
        except Exception as e:
            print('edit()', e)
        finally:
            pass

    def delete(self):
        try:
            values = values = self.get_entry_values()
            result = delete_element_by_id(self.frame_code, values[0])
            if (result):
                showinfo(title='Success', message='Xóa ' + self.frame_name + ' thành công!')
                self.get_all()
            else:
                showerror(title='Error', message='Xóa ' + self.frame_name + ' thất bại!')
        except Exception as e:
            print('delete()', e)
        finally:
            pass

    # Populate data
    def get_all(self):
        try:
            # Clear the treeview list items
            for item in self.tree.get_children():
                self.tree.delete(item)

            result = get_element_list(self.frame_code)
            if (not result or len(result) == 0):
                showerror(title='Error', message='Không có dữ liệu.')
            else:
                rows = []
                for row in result:
                    parsed_row = self.parse_row(row)
                    rows.append(tuple(parsed_row))
                for row in rows:
                    self.tree.insert('', tk.END, values=row)
        except Exception as e:
            print('get_all()', e)
            pass

    def call_apis(self):
        self.get_cb_values()
        self.get_all()
