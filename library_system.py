import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from api import *

# # Find books
# def search_button():
#     try:
#         dellist(tree)
#         val = searchEntry.get()
#         if (str(val).isnumeric()):
#             values = get_object_by_id('book', val)
#         else:
#             values = get_objects_by_name('book', val)
#         if (not values or len(values) == 0):
#             tk.messagebox.showinfo(title='Hi', message='Không có sách như tìm kiếm')
#         else:
#             results = []
#             for item in values:
#                 results.append(tuple(item))
#             for result in results:
#                 tree.insert('', tk.END, values=result)
#     except Exception as e:
#         pass
#     finally:
#         searchEntry.delete(0, 'end')

# # Import books
# #@log
# def importbook_button():

#     def item_selected(event): # hàm lựa chọn sách trên bảng
#         for selected_item in tree.selection():
#             item = tree.item(selected_item)
#             record = item['values']
#     def add_book_to_db(): # hàm lựa chọn sách trên bảng rồi thêm vào db
#         for selected_item in tree.selection():
#             item = tree.item(selected_item)
#             record = item.get("values")
#             record[0] = str(record[0])
#             try:
#                 result = append_object('book', record)
#                 if (result):
#                     tk.messagebox.showinfo(title='Hi', message='Thêm sách thành công!')
#                 else:
#                     tk.messagebox.showerror(title='Hi', message='Thêm sách thất bại!')
#             except Exception as e:
#                 print(e)
#             finally:
#                 pass

#     # Đọc data từ file excel
#     data = xlrd.open_workbook('book.xls')
#     sheet = data.sheet_by_index(0)
#     for row in range(1, sheet.nrows):
#         row_values = ()
#         for cell in range(sheet.ncols):
#             cell_value = sheet.row_values(row)[cell]
#             if (isinstance(cell_value, float)):
#                 row_values += (int(cell_value),)
#             else:
#                 row_values += (cell_value,)
#         try:
#             tree.insert('', tk.END, values=row_values)
#         except Exception:
#             pass

#     tree.bind('<<TreeviewSelect>>', item_selected)

#     # nút xác nhận chọn sách để đưa vào db
#     btn_select = tk.Button(importwindow, text='Nhập sách', command=add_book_to_db)
#     btn_select.place(x=1100, y=100)

# #@log
# def lend_book():

#     def toggle(button, state):
#         if (button["state"] == "normal" and state == 'disabled'):
#             button["state"] = "disabled"
#             button["text"] = "enable"
#         if (button["state"] == "disabled" and state == 'enabled'):
#             button["state"] = "normal"
#             button["text"] = "disable"

#     def checklc_button():
#         values = get_object_by_id('lc', entry_card_id.get())
#         if (not values):
#             tk.messagebox.showerror(title='Error', message='Thẻ thư viện không hợp lệ!')
#             toggle(btn_append, 'disabled')
#         else:
#             tk.messagebox.showinfo(title='Thông Báo', message='Thẻ thư viện hợp lệ!')
#             toggle(btn_append, 'enabled')
    
#     editwindow = tk.Toplevel()
#     editwindow.title('Mượn sách')
#     editwindow.geometry('450x300+800+300')
#     editwindow.resizable(0, 0)

#     var = tk.StringVar()
#     tk.Label(editwindow, text='Mã thẻ:').place(x=50, y=20)
#     tk.Label(editwindow, text='Mã sách:').place(x=50, y=90)
#     tk.Label(editwindow, text='Tên sách:').place(x=50, y=130)
#     tk.Label(editwindow, text='Ngày mượn:').place(x=50, y=170)
#     tk.Label(editwindow, text='Ngày cần trả:').place(x=50, y=210)

#     val_eb = tk.StringVar()
#     val_ec = tk.StringVar()
#     val_ep = tk.StringVar()
#     val_es = tk.StringVar()
#     val_el = tk.StringVar()
    
#     entry_card_id = tk.Entry(editwindow, textvariable=val_eb)
#     entry_book_id = tk.Entry(editwindow, textvariable=val_ec)
#     entry_book_name = tk.Entry(editwindow, textvariable=val_ep)
#     entry_lend_date = tk.Entry(editwindow, textvariable=val_es)
#     entry_return_date = tk.Entry(editwindow, textvariable=val_el)

#     entry_card_id.place(x=160, y=20)
#     entry_book_id.place(x=160, y=90)
#     entry_book_name.place(x=160, y=130)
#     entry_lend_date.place(x=160, y=170)
#     entry_return_date.place(x=160, y=210)

#     btn_append = tk.Button(editwindow, text='Cho mượn', command=appendbook_button)
#     btn_append.place(x=150, y=260)
#     btn_check = tk.Button(editwindow, text='Kiểm tra thẻ', command=checklc_button)
#     btn_check.place(x=170, y=50)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        def no_func():
            print('Nothing here')

        def hide_all_frames():
            for widget in about_frame.winfo_children():
                widget.destroy()
            for widget in book_frame.winfo_children():
                widget.destroy()
            about_frame.pack_forget()
            book_frame.pack_forget()

        # About
        about_frame = ttk.Frame(self)

        def about():
            hide_all_frames()
            about_frame.pack(fill="both", expand=1)
            create_about_widgets()

        def create_about_widgets():
            label = ttk.Label(about_frame, text='Author: Nguyễn Kim Cương')
            label.pack(ipadx=0, ipady=20)

        # Book
        book_frame = ttk.Frame(self)
        book_frame.columnconfigure(0, weight=1)
        book_frame.columnconfigure(1, weight=3)
        book_frame.rowconfigure(0, weight=1)
        
        book_label = ['Mã sách', 'Tên sách', 'Mã NXB', 'Mã tác giả', 'Mã TLS', 'Mã vị trí', 'Năm XB', 'SL tổng', 'SL tồn kho', 'Đơn giá']
        book_var = []
        for i in range(len(book_label)):
            book_var.append(tk.StringVar())

        # class book_label:
        #     id = 'Mã sách'
        #     name = 'Tên sách'
        #     publisher_id = 'Mã NXB'
        #     author_id = 'Mã tác giả'
        #     category_id = 'Mã TLS'
        #     position_id = 'Mã vị trí'
        #     published_year = 'Năm XB'
        #     total_amount = 'SL tổng'
        #     available_amount = 'SL tồn kho'
        #     price = 'Đơn giá'

        def manage_book():
            hide_all_frames()
            book_frame.pack(fill="both", expand=1)
            create_book_widgets()

        def create_book_widgets():
            # Set variable values
            # for i in range(len(book_label)):
            #     book_var[i].set('placeholder')

            # Left menu
            menu_left = tk.Frame(book_frame, highlightbackground='#ababab', highlightthickness=1)
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
            for i in range(len(book_label)):
                label_arr.append(ttk.Label(menu_upper_left, text=book_label[i]))
                label_arr[i].grid(column=0, row=i, sticky=tk.W, padx=(10, 0), pady=10)
                entry_arr.append(ttk.Entry(menu_upper_left, textvariable=book_var[i]))
                entry_arr[i].grid(column=1, row=i, sticky=tk.EW, padx=(0, 10), pady=10)

            # Lower left menu
            menu_lower_left = tk.Frame(menu_left)
            menu_lower_left.columnconfigure(0, weight=1)
            menu_lower_left.columnconfigure(1, weight=1)
            menu_lower_left.rowconfigure(0, weight=1)
            menu_lower_left.rowconfigure(1, weight=1)

            menu_lower_left.grid(column=0, row=1, sticky=tk.NSEW)

            def button_clicked():
                print('clicked')
                button.state(['disabled'])

            button = ttk.Button(menu_lower_left, text='Tìm', compound=tk.LEFT, command=button_clicked)
            button.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

            button = ttk.Button(menu_lower_left, text='Thêm', compound=tk.LEFT, command=button_clicked)
            button.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

            button = ttk.Button(menu_lower_left, text='Sửa', compound=tk.LEFT, command=button_clicked)
            button.grid(column=0, row=1, sticky=tk.NSEW, padx=10, pady=10)

            button = ttk.Button(menu_lower_left, text='Xóa', compound=tk.LEFT, command=button_clicked)
            button.grid(column=1, row=1, sticky=tk.NSEW, padx=10, pady=10)

            # Right menu
            menu_right = tk.Frame(book_frame, highlightbackground='#ababab', highlightthickness=1)
            menu_right.columnconfigure(0, weight=1)
            menu_right.columnconfigure(1, weight=0)
            menu_right.rowconfigure(0, weight=1)

            menu_right.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

            text = tk.Text(menu_right, height=10)
            text.grid(column=0, row=0, sticky=tk.NSEW)

            scrollbar = ttk.Scrollbar(menu_right, orient='vertical', command=text.yview)
            scrollbar.grid(column=1, row=0, sticky=tk.NS)

            text['yscrollcommand'] = scrollbar.set

            for i in range(1,50):
                position = f'{i}.0'
                text.insert(position,f'Line {i}\n')

        # Root window
        self.title('Hệ thống quản lý thư viện')
        self.geometry('1280x720')
        # self.resizable(False, False)
        self.iconbitmap('./assets/book.ico')

        # Create a menubar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Create a menu
        home_menu = tk.Menu(menubar, tearoff=0)
        # Add the File menu to the menubar
        menubar.add_cascade(label='Home', menu=home_menu)
        # Add menu items to the menu
        home_menu.add_command(label='About', command=about)
        home_menu.add_separator()
        home_menu.add_command(label='Exit', command=self.destroy)

        config_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Quản lý cấu hình', menu=config_menu)
        config_menu.add_command(label='Quản lý nhà xuất bản', command=no_func)
        config_menu.add_command(label='Quản lý tác giả', command=no_func)
        config_menu.add_command(label='Quản lý thể loại sách', command=no_func)
        config_menu.add_command(label='Quản lý vị trí giá sách', command=no_func)

        lc_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Quản lý độc giả', menu=lc_menu)
        lc_menu.add_command(label='Quản lý thẻ thư viện', command=no_func)
        lc_menu.add_separator()
        lc_menu.add_command(label='Cấp lại thẻ thư viện', command=no_func)

        book_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Quản lý đầu sách', menu=book_menu)
        book_menu.add_command(label='Quản lý sách', command=manage_book)
        book_menu.add_separator()
        book_menu.add_command(label='Lập đơn mua sách', command=no_func)
        book_menu.add_command(label='Lập đơn hủy sách', command=no_func)

        lend_return_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Quản lý mượn trả', menu=lend_return_menu)
        lend_return_menu.add_command(label='Quản lý phiếu mượn', command=no_func)
        lend_return_menu.add_command(label='Quản lý phiếu trả', command=no_func)

        report_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Báo cáo/thống kê', menu=report_menu)
        report_menu.add_command(label='Thống kê số lượng sách', command=no_func)
        report_menu.add_command(label='Thống kê thể loại sách được mượn', command=no_func)
        report_menu.add_command(label='Thống kê sách quá hạn', command=no_func)
        report_menu.add_command(label='Thống kê độc giả', command=no_func)

if __name__ == '__main__':
    app = App()
    app.mainloop()
