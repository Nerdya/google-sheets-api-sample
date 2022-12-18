import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
from apis.google_sheets_api import *

class ReturnBookFrame(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        # Configure frame
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=3)
        self.rowconfigure(0, weight=1)

        # Variables
        self.frame_code = 'return_slip'
        self.frame_name = 'phiếu trả'
        self.columns = ('id', 'library_card_id', 'return_date')
        self.column_widths = [80, 40, 80]    # 860
        self.labels = ['Mã phiếu trả', 'Mã thẻ', 'Ngày trả']
        self.vars = []
        for i in range(len(self.labels)):
            self.vars.append(tk.StringVar())
        self.search_var = tk.StringVar()
        self.label_arr = []
        self.entry_arr = []

        # Variables_2
        self.frame_code_2 = 'return_slip_detail'
        self.frame_name_2 = 'CT phiếu trả'
        self.columns_2 = ('id', 'book_id')
        self.column_widths_2 = [80, 160]    # 860
        self.labels_2 = ['Mã phiếu trả', 'Mã sách']
        self.vars_2 = []
        for i in range(len(self.labels_2)):
            self.vars_2.append(tk.StringVar())
        self.search_var_2 = tk.StringVar()
        self.label_arr_2 = []
        self.entry_arr_2 = []

        # Combobox variables
        # self.cb_index_arr = [2, 3, 4, 5]
        # self.cb_object_names = ['publisher', 'author', 'category', 'position']
        # self.id_list_arr = {
        #     'publisher': [],
        #     'author': [],
        #     'category': [],
        #     'position': []
        # }
        # self.value_list_arr = {
        #     'publisher': [],
        #     'author': [],
        #     'category': [],
        #     'position': []
        # }

        ### Left panel

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

        button_search = ttk.Button(menu_upper_left, text='Tìm mã ' + self.frame_name, compound=tk.LEFT, command=lambda: self.search(self.tree, 'id', self.search_var, self.frame_code))
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
            # if (not i in self.cb_index_arr):
            self.entry_arr.append(ttk.Entry(menu_middle_left, textvariable=self.vars[i]))
            # else:
                # self.entry_arr.append(ttk.Combobox(menu_middle_left, textvariable=self.vars[i]))
                # match i:
                #     case 2:
                #         self.entry_arr[i]['values'] = self.value_list_arr['publisher']
                #     case 3:
                #         self.entry_arr[i]['values'] = self.value_list_arr['author']
                #     case 4:
                #         self.entry_arr[i]['values'] = self.value_list_arr['category']
                #     case 5:
                #         self.entry_arr[i]['values'] = self.value_list_arr['position']
                # self.entry_arr[i]['state'] = 'readonly'
            self.entry_arr[i].grid(column=1, row=i, sticky=tk.EW, padx=(0, 10), pady=10)

        # Lower left menu
        menu_lower_left = tk.Frame(menu_left, highlightbackground='#ababab', highlightthickness=1)
        menu_lower_left.columnconfigure(0, weight=1)
        menu_lower_left.columnconfigure(1, weight=1)
        menu_lower_left.columnconfigure(2, weight=1)
        menu_lower_left.rowconfigure(0, weight=1)

        menu_lower_left.grid(column=0, row=2, sticky=tk.NSEW)

        button_add = ttk.Button(menu_lower_left, text='Thêm', compound=tk.LEFT, command=lambda: self.add(self.tree, self.vars, self.frame_code, self.frame_name, False))
        button_add.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

        button_edit = ttk.Button(menu_lower_left, text='Sửa', compound=tk.LEFT, command=lambda: self.edit(self.tree, self.vars, self.frame_code, self.frame_name, False))
        button_edit.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

        button_delete = ttk.Button(menu_lower_left, text='Xóa', compound=tk.LEFT, command=lambda: self.delete(self.tree, self.vars, self.frame_code, self.frame_name, False))
        button_delete.grid(column=2, row=0, sticky=tk.NSEW, padx=10, pady=10)
        button_delete["state"] = "disabled"

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

        def item_selected(event):
            for selected_item in self.tree.selection():
                item = self.tree.item(selected_item)
                record = item['values']
                for i in range(len(self.vars)):
                    self.vars[i].set(record[i])
                self.search(self.tree_2, 'id', self.vars[0], self.frame_code_2)
                self.vars_2[0].set(self.vars[0].get())

        # Selection event
        self.tree.bind('<<TreeviewSelect>>', item_selected)

        self.tree.grid(row=0, column=0, sticky=tk.NSEW)

        scrollbar = ttk.Scrollbar(menu_right, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(column=1, row=0, sticky=tk.NS)

        ### Right panel

        # Left menu
        menu_left_2 = tk.Frame(self)
        menu_left_2.columnconfigure(0, weight=1)
        menu_left_2.rowconfigure(0, weight=0)
        menu_left_2.rowconfigure(1, weight=1)
        menu_left_2.rowconfigure(2, weight=0)

        menu_left_2.grid(column=2, row=0, sticky=tk.NSEW, padx=(10, 0), pady=10)

        # Upper left menu
        menu_upper_left_2 = tk.Frame(menu_left_2, highlightbackground='#ababab', highlightthickness=1)
        # menu_upper_left_2.columnconfigure(0, weight=2)
        # menu_upper_left_2.columnconfigure(1, weight=1)
        menu_upper_left_2.columnconfigure(0, weight=1)
        menu_upper_left_2.rowconfigure(0, weight=1)
        
        menu_upper_left_2.grid(column=0, row=0, sticky=tk.NSEW)

        label_2 = ttk.Label(menu_upper_left_2, text='Nhấn vào dòng phiếu trả để hiển thị chi tiết')
        label_2.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

        # entry_search_2 = ttk.Entry(menu_upper_left_2, textvariable=self.search_var_2)
        # entry_search_2.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

        # button_search_2 = ttk.Button(menu_upper_left_2, text='Tìm tên ' + self.frame_name_2, compound=tk.LEFT, command=lambda: self.search(self.tree_2, self.search_var_2, self.frame_code_2))
        # button_search_2.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

        # Middle left menu
        menu_middle_left_2 = tk.Frame(menu_left_2, highlightbackground='#ababab', highlightthickness=1)
        menu_middle_left_2.columnconfigure(0, weight=1)
        menu_middle_left_2.columnconfigure(1, weight=2)
        menu_middle_left_2.rowconfigure(10, weight=1)
        
        menu_middle_left_2.grid(column=0, row=1, sticky=tk.NSEW, pady=10)

        # Populate label and entry arrays
        for i in range(len(self.labels_2)):
            self.label_arr_2.append(ttk.Label(menu_middle_left_2, text=self.labels_2[i]))
            self.label_arr_2[i].grid(column=0, row=i, sticky=tk.W, padx=10, pady=10)
            # if (not i in self.cb_index_arr_2):
            self.entry_arr_2.append(ttk.Entry(menu_middle_left_2, textvariable=self.vars_2[i]))
            # else:
                # self.entry_arr_2.append(ttk.Combobox(menu_middle_left_2, textvariable=self.vars_2[i]))
                # match i:
                #     case 2:
                #         self.entry_arr_2[i]['values'] = self.value_list_arr_2['publisher']
                #     case 3:
                #         self.entry_arr_2[i]['values'] = self.value_list_arr_2['author']
                #     case 4:
                #         self.entry_arr_2[i]['values'] = self.value_list_arr_2['category']
                #     case 5:
                #         self.entry_arr_2[i]['values'] = self.value_list_arr_2['position']
                # self.entry_arr_2[i]['state'] = 'readonly'
            self.entry_arr_2[i].grid(column=1, row=i, sticky=tk.EW, padx=(0, 10), pady=10)
        
        # Set id entry readonly
        self.entry_arr_2[0]['state'] = 'readonly'

        # Lower left menu
        menu_lower_left_2 = tk.Frame(menu_left_2, highlightbackground='#ababab', highlightthickness=1)
        menu_lower_left_2.columnconfigure(0, weight=1)
        menu_lower_left_2.columnconfigure(1, weight=1)
        menu_lower_left_2.columnconfigure(2, weight=1)
        menu_lower_left_2.rowconfigure(0, weight=1)

        menu_lower_left_2.grid(column=0, row=2, sticky=tk.NSEW)

        button_add_2 = ttk.Button(menu_lower_left_2, text='Thêm', compound=tk.LEFT, command=lambda: self.add(self.tree_2, self.vars_2, self.frame_code_2, self.frame_name_2, True, self.vars_2[0]))
        button_add_2.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

        button_edit_2 = ttk.Button(menu_lower_left_2, text='Sửa', compound=tk.LEFT, command=lambda: self.edit(self.tree_2, self.vars_2, self.frame_code_2, self.frame_name_2, True, self.vars_2[0]))
        button_edit_2.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

        button_delete_2 = ttk.Button(menu_lower_left_2, text='Xóa', compound=tk.LEFT, command=lambda: self.delete(self.tree_2, self.vars_2, self.frame_code_2, self.frame_name_2, True, self.vars_2[0]))
        button_delete_2.grid(column=2, row=0, sticky=tk.NSEW, padx=10, pady=10)

        # Right menu
        menu_right_2 = tk.Frame(self, highlightbackground='#ababab', highlightthickness=1)
        menu_right_2.columnconfigure(0, weight=1)
        menu_right_2.columnconfigure(1, weight=0)
        menu_right_2.rowconfigure(0, weight=1)

        menu_right_2.grid(column=3, row=0, sticky=tk.NSEW, padx=10, pady=10)

        self.tree_2 = ttk.Treeview(menu_right_2, columns=self.columns_2, show='headings')

        # Define headings
        for i in range(len(self.columns_2)):
            self.tree_2.heading(self.columns_2[i], text=self.labels_2[i])

        # Customize columns
        for i in range(len(self.columns_2)):
            self.tree_2.column(self.columns_2[i], width=self.column_widths_2[i], anchor=tk.W)

        def item_selected_2(event):
            for selected_item in self.tree_2.selection():
                item = self.tree_2.item(selected_item)
                record = item['values']
                for i in range(len(self.vars_2)):
                    self.vars_2[i].set(record[i])

        # Selection event
        self.tree_2.bind('<<TreeviewSelect>>', item_selected_2)

        self.tree_2.grid(row=0, column=0, sticky=tk.NSEW)

        scrollbar_2 = ttk.Scrollbar(menu_right_2, orient='vertical', command=self.tree_2.yview)
        self.tree_2.configure(yscroll=scrollbar_2.set)
        scrollbar_2.grid(column=1, row=0, sticky=tk.NS)

    # def cb_id_to_value(self, object_name, id):
    #     for i in range(len(self.id_list_arr[object_name])):
    #         if (id == self.id_list_arr[object_name][i]):
    #             return self.value_list_arr[object_name][i]
    #     return ''

    # def cb_value_to_id(self, object_name, value):
    #     for i in range(len(self.value_list_arr[object_name])):
    #         if (value == self.value_list_arr[object_name][i]):
    #             return self.id_list_arr[object_name][i]
    #     return ''

    def parse_row(self, row):
        parsed_row = []
        for i in range(len(row)):
            # if (not i in self.cb_index_arr):
            parsed_row.append(row[i])
            # else:
            #     object_name = self.cb_object_names[i - 2]
            #     parsed_row.append(self.cb_id_to_value(object_name, row[i]))
        return parsed_row

    def get_entry_values(self, vars):
        values = []
        for i in range(len(vars)):
            # if (not i in self.cb_index_arr):
            values.append(vars[i].get())
            # else:
            #     object_name = self.cb_object_names[i - 2]
            #     values.append(self.cb_value_to_id(object_name, self.vars[i].get()))
        return values

    # Get combobox values
    # def get_cb_values(self):
    #     try:
    #         for object_name in self.cb_object_names:
    #             result = get_element_list(object_name)
    #             if (not result or len(result) == 0):
    #                 showerror(title='Error', message='Không có dữ liệu.')
    #             else:
    #                 for row in result:
    #                     self.id_list_arr[object_name].append(row[0])
    #                     self.value_list_arr[object_name].append(row[1])
    #     except Exception as e:
    #         print('get_cb_values()', e)
    #         pass

    def search(self, tree, type, search_var, frame_code):
        try:
            # Clear the treeview list items
            for item in tree.get_children():
                tree.delete(item)
            search_value = ''
            if (search_var):
                search_value = search_var.get()
            result = get_element_list_by(frame_code, type, search_value)
            if (not result or len(result) == 0):
                showerror(title='Error', message='Không có dữ liệu.')
            else:
                rows = []
                for row in result:
                    parsed_row = self.parse_row(row)
                    rows.append(tuple(parsed_row))
                for row in rows:
                    tree.insert('', tk.END, values=row)
        except Exception as e:
            print('search()', e)
            pass

    def add(self, tree, vars, frame_code, frame_name, allow_duplicate_ids, id_var = None):
        try:
            values = self.get_entry_values(vars)
            # Check if book id is duplicated (if allow_duplicate_ids sets to True)
            if (allow_duplicate_ids):
                object = parse_object_name(frame_code)
                if (object == None): return False
                find_result = find_element_by(object, 'name', values[1])
                if (find_result[0]):
                    print('Book id already exists!')
                    showerror(title='Error', message='Thêm ' + frame_name + ' thất bại!')
                    return
            result = append_element(frame_code, values, allow_duplicate_ids)
            if (result):
                showinfo(title='Success', message='Thêm ' + frame_name + ' thành công!')
                if (id_var):
                    self.search(tree, 'id', id_var, frame_code)
                else:
                    self.get_all(tree, frame_code)
            else:
                showerror(title='Error', message='Thêm ' + frame_name + ' thất bại!')
        except Exception as e:
            print('add()', e)
        finally:
            pass

    def edit(self, tree, vars, frame_code, frame_name, allow_duplicate_ids, id_var = None):
        try:
            values = values = self.get_entry_values(vars)
            # Check if book id is duplicated (if allow_duplicate_ids sets to True)
            if (allow_duplicate_ids):
                object = parse_object_name(frame_code)
                if (object == None): return False
                find_result = find_element_by(object, 'name', values[1])
                if (find_result[0]):
                    print('Book id already exists!')
                    showerror(title='Error', message='Thêm ' + frame_name + ' thất bại!')
                    return
            result = update_element(frame_code, values)
            if (result):
                showinfo(title='Success', message='Sửa ' + frame_name + ' thành công!')
                if (id_var):
                    self.search(tree, 'id', id_var, frame_code)
                else:
                    self.get_all(tree, frame_code)
            else:
                showerror(title='Error', message='Sửa ' + frame_name + ' thất bại!')
        except Exception as e:
            print('edit()', e)
        finally:
            pass

    def delete(self, tree, vars, frame_code, frame_name, allow_duplicate_ids, id_var = None):
        try:
            values = values = self.get_entry_values(vars)
            # Check if book id is duplicated (if allow_duplicate_ids sets to True)
            # if (allow_duplicate_ids):
            #     object = parse_object_name(frame_code)
            #     if (object == None): return False
            #     find_result = find_element_by(object, 'name', values[1])
            #     if (find_result[0]):
            #         print('Book id already exists!')
            #         showerror(title='Error', message='Xóa ' + frame_name + ' thất bại!')
            #         return
            result = delete_element_by(frame_code, 'name', values[1])
            if (result):
                showinfo(title='Success', message='Xóa ' + frame_name + ' thành công!')
                if (id_var):
                    self.search(tree, 'id', id_var, frame_code)
                else:
                    self.get_all(tree, frame_code)
            else:
                showerror(title='Error', message='Xóa ' + frame_name + ' thất bại!')
        except Exception as e:
            print('delete()', e)
        finally:
            pass

    # Populate data
    def get_all(self, tree, frame_code):
        try:
            # Clear the treeview list items
            for item in tree.get_children():
                tree.delete(item)

            result = get_element_list(frame_code)
            if (not result or len(result) == 0):
                showerror(title='Error', message='Không có dữ liệu.')
            else:
                rows = []
                for row in result:
                    parsed_row = self.parse_row(row)
                    rows.append(tuple(parsed_row))
                for row in rows:
                    tree.insert('', tk.END, values=row)
        except Exception as e:
            print('get_all()', e)
            pass

    def call_apis(self):
        # self.get_cb_values()
        self.get_all(self.tree, self.frame_code)
