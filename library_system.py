import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
from apis.google_sheets_api import *
from modules.AboutFrame import AboutFrame
from modules.AuthorFrame import AuthorFrame
from modules.BookFrame import BookFrame
from modules.CategoryFrame import CategoryFrame
from modules.ImportBookFrame import ImportBookFrame
from modules.LendBookFrame import LendBookFrame
from modules.LibraryCardFrame import LibraryCardFrame
from modules.LoadingFrame import LoadingFrame
from modules.PositionFrame import PositionFrame
from modules.PublisherFrame import PublisherFrame
from modules.ReissueLibraryCardFrame import ReissueLibraryCardFrame
from modules.RemoveBookFrame import RemoveBookFrame
from modules.ReportBookFrame import ReportBookFrame
from modules.ReportLendedBookFrame import ReportLendedBookFrame
from modules.ReportLibraryCardFrame import ReportLibraryCardFrame
from modules.ReportOverdueBookFrame import ReportOverdueBookFrame
from modules.ReturnBookFrame import ReturnBookFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Root window
        self.title('Hệ thống quản lý thư viện')
        self.geometry('1280x720')
        # self.resizable(False, False)
        self.iconbitmap('./assets/book.ico')

        # Container frame
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}
        for F in (
            AboutFrame,
            AuthorFrame,
            BookFrame,
            CategoryFrame,
            ImportBookFrame,
            LendBookFrame,
            LibraryCardFrame,
            LoadingFrame,
            PositionFrame,
            PublisherFrame,
            ReissueLibraryCardFrame,
            RemoveBookFrame,
            ReportBookFrame,
            ReportLendedBookFrame,
            ReportLibraryCardFrame,
            ReportOverdueBookFrame,
            ReturnBookFrame
        ):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(column=0, row=0, sticky=tk.NSEW)

        # Loading frame
        self.loading_frame = LoadingFrame(container, self)
        self.loading_frame.grid(column=0, row=0, sticky=tk.NSEW)

        # Default frame
        self.show_frame(AboutFrame)

        # Create a menubar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Create a menu
        home_menu = tk.Menu(menubar, tearoff=0)
        # Add menu to the menubar
        menubar.add_cascade(label='Home', menu=home_menu)
        # Add menu items to the menu
        home_menu.add_command(label='About', command=lambda: self.show_frame(AboutFrame))
        home_menu.add_separator()
        home_menu.add_command(label='Exit', command=self.destroy)

        config_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Quản lý cấu hình', menu=config_menu)
        config_menu.add_command(label='Quản lý nhà xuất bản', command=lambda: self.show_frame(PublisherFrame))
        config_menu.add_command(label='Quản lý tác giả', command=lambda: self.show_frame(AuthorFrame))
        config_menu.add_command(label='Quản lý thể loại sách', command=lambda: self.show_frame(CategoryFrame))
        config_menu.add_command(label='Quản lý vị trí giá sách', command=lambda: self.show_frame(PositionFrame))

        lc_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Quản lý độc giả', menu=lc_menu)
        lc_menu.add_command(label='Quản lý thẻ thư viện', command=lambda: self.show_frame(LibraryCardFrame))
        lc_menu.add_separator()
        lc_menu.add_command(label='Cấp lại thẻ thư viện', command=lambda: self.show_frame(ReissueLibraryCardFrame))

        book_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Quản lý đầu sách', menu=book_menu)
        book_menu.add_command(label='Quản lý sách', command=lambda: self.show_frame(BookFrame))
        book_menu.add_separator()
        book_menu.add_command(label='Lập đơn mua sách', command=lambda: self.show_frame(ImportBookFrame))
        book_menu.add_command(label='Lập đơn hủy sách', command=lambda: self.show_frame(RemoveBookFrame))

        lend_return_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Quản lý mượn trả', menu=lend_return_menu)
        lend_return_menu.add_command(label='Quản lý phiếu mượn', command=lambda: self.show_frame(LendBookFrame))
        lend_return_menu.add_command(label='Quản lý phiếu trả', command=lambda: self.show_frame(ReturnBookFrame))

        report_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Báo cáo/thống kê', menu=report_menu)
        report_menu.add_command(label='Thống kê số lượng sách', command=lambda: self.show_frame(ReportBookFrame))
        report_menu.add_command(label='Thống kê thể loại sách được mượn', command=lambda: self.show_frame(ReportLendedBookFrame))
        report_menu.add_command(label='Thống kê sách quá hạn', command=lambda: self.show_frame(ReportOverdueBookFrame))
        report_menu.add_command(label='Thống kê độc giả', command=lambda: self.show_frame(ReportLibraryCardFrame))
    
    def show_frame(self, container):
        # Call requested frame
        frame = self.frames[container]
        # Show loading frame
        self.loading_frame.tkraise()
        # Set cursor busy
        self.config(cursor="wait")
        self.update()
        # Call frame's apis
        frame.call_apis()
        # Set cursor unset
        self.config(cursor="")
        # Show frame
        frame.tkraise()
    
if __name__ == '__main__':
    app = App()
    app.mainloop()
