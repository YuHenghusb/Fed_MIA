import tkinter as tk
from tkinter import messagebox
import pymysql
import read

class mysql:
    def __init__(self):
        self.cnn = pymysql.connect(
            host='rm-cn-zpr373ey2000qsoo.rwlb.rds.aliyuncs.com',
            user='e_book',
            password='E-book21xa',
            port=3306,
            database='e_book_date',
            charset='utf8'
        )
        self.cursor = self.cnn.cursor()

    def search(self, table, column1, column2, value1, value2):
        self.cursor.execute("SELECT * FROM `{}` WHERE `{}` like %s or `{}` like %s".format(table, column1, column2), ['%'+value1+'%', '%'+value2+'%'])
        result = self.cursor.fetchall()
        return result

    def drop(self, tablename):
        self.cursor.execute("DROP TABLE `{}`".format(tablename))
        self.cnn.commit()

    def delete(self, table, column, name):
        self.cursor.execute("DELETE FROM `{}` WHERE `{}`=%s".format(table, column), name)
        self.cnn.commit()

    def inquire(self, table, column, st, value):
        self.cursor.execute("SELECT * FROM `{}` WHERE `{}`{}%s".format(table, column, st), value)
        result = self.cursor.fetchall()
        return result

    def add(self, book_name, author_name, lorder_name):
        self.cursor.execute("INSERT INTO book_date (book_name, author_name, lorder) VALUES(%s, %s, %s)", (book_name, author_name, lorder_name))
        self.cnn.commit()

    def update(self, book_name, state):
        self.cursor.execute("UPDATE users_uplord SET state=%s WHERE book_name=%s", (state, book_name))
        self.cnn.commit()

    def close(self):
        self.cursor.close()
        self.cnn.close()

class mainpage:
    def __init__(self, root, username):

        self.frame_top = tk.Frame(root, relief='groove')
        self.label = tk.Label(self.frame_top, text='欢迎'+username)
        self.label.pack(side='left')
        self.frame_top.pack(side='top', fill='x')

        self.frame_bottom = tk.Frame(root)
        self.search = tk.Button(self.frame_bottom, relief='raised', text='搜索书籍', command=lambda: self.change(self.frame_search_book, self.search), state='disabled')
        self.search.grid(row=0, column=0, sticky='ew')
        self.bookrack = tk.Button(self.frame_bottom, relief='raised', text='搜索用户', command=lambda: self.change(self.frame_search_user, self.bookrack))
        self.bookrack.grid(row=0, column=1, sticky='ew')
        self.message = tk.Button(self.frame_bottom, relief='raised', text='审核书籍', command=lambda: (self.change(self.frame_check, self.message), self.lord_record(root, '=', 'new', username)))
        self.message.grid(row=0, column=2, sticky='ew')
        self.mine = tk.Button(self.frame_bottom, relief='raised', text='我的')
        self.mine.grid(row=0, column=3, sticky='ew')
        self.frame_bottom.columnconfigure(0, weight=1)
        self.frame_bottom.columnconfigure(1, weight=1)
        self.frame_bottom.columnconfigure(2, weight=1)
        self.frame_bottom.columnconfigure(3, weight=1)
        self.frame_bottom.pack(side='bottom', fill='x')

        self.frame_search_book = tk.Frame(root)
        self.search_e = tk.Entry(self.frame_search_book)
        self.search_e.grid(row=0, column=0, sticky='new')
        self.search_b = tk.Button(self.frame_search_book, text='搜索', relief='raised', command=lambda: self.search_book(root, username))
        self.search_b.grid(row=0, column=1, sticky='ne')
        self.canvas = tk.Canvas(self.frame_search_book)
        self.scrollbar = tk.Scrollbar(self.frame_search_book, orient='vertical', command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=1, column=0, sticky='nsew')
        self.scrollbar.grid(row=1, column=1, sticky='ns')
        self.canvas.bind('<Configure>', self.on_canvas_resize)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.frame_search_book.grid_rowconfigure(1, weight=1)
        self.frame_search_book.grid_columnconfigure(0, weight=1)
        self.frame_search_book.pack(fill='both', expand=True)

        self.frame_search_user = tk.Frame(root)
        self.search_eu = tk.Entry(self.frame_search_user)
        self.search_eu.grid(row=0, column=0, sticky='new')
        self.search_bu = tk.Button(self.frame_search_user, text='搜索', relief='raised', command=lambda: self.search_user())
        self.search_bu.grid(row=0, column=1, sticky='ne')
        self.canvas_ = tk.Canvas(self.frame_search_user)
        self.scrollbar_ = tk.Scrollbar(self.frame_search_user, orient='vertical', command=self.canvas_.yview)
        self.canvas_.config(yscrollcommand=self.scrollbar_.set)
        self.canvas_.grid(row=1, column=0, sticky='nsew')
        self.scrollbar_.grid(row=1, column=1, sticky='ns')
        self.canvas_.bind('<Configure>', self.on_canvas_resize)
        self.canvas_.bind_all("<MouseWheel>", self.on_mousewheel)
        self.frame_search_user.grid_rowconfigure(1, weight=1)
        self.frame_search_user.grid_columnconfigure(0, weight=1)

        self.frame_check = tk.Frame(root)
        self.button1 = tk.Button(self.frame_check, text='未处理', command=lambda: self.lord_record(root, '=', 'new', username))
        self.button1.grid(row=0, columnspan=2, sticky='we')
        self.button2 = tk.Button(self.frame_check, text='已处理', command=lambda: self.lord_record(root, '!=', 'new', username))
        self.button2.grid(row=1, columnspan=2, sticky='we')
        self.lable_lord = tk.Label(self.frame_check, text='用户上传记录及状态')
        self.lable_lord.grid(row=2, columnspan=2, sticky='we')
        self.canvas_lord = tk.Canvas(self.frame_check)
        self.scrollbar_lord = tk.Scrollbar(self.frame_check, orient='vertical', command=self.canvas_lord.yview)
        self.canvas_lord.config(yscrollcommand=self.scrollbar_lord.set)
        self.canvas_lord.grid(row=3, column=0, sticky='nsew')
        self.scrollbar_lord.grid(row=3, column=1, sticky='ns')
        self.canvas_lord.bind('<Configure>', self.on_canvas_resize)
        self.canvas_lord.bind_all("<MouseWheel>", self.on_mousewheel)
        self.frame_check.grid_rowconfigure(3, weight=1)
        self.frame_check.grid_columnconfigure(0, weight=1)

        self.frame_mine = tk.Frame(root)

    def change(self, frame2, button2):
        self.frame_search_user.pack_forget()
        self.frame_search_book.pack_forget()
        self.frame_check.pack_forget()
        self.frame_mine.pack_forget()
        self.search['state'] = 'normal'
        self.bookrack['state'] = 'normal'
        self.message['state'] = 'normal'
        self.mine['state'] = 'normal'
        button2['state'] = 'disabled'
        frame2.pack(fill='both', expand=True)

    def on_canvas_resize(self, event):
        canvas_width = event.width
        for item in self.canvas.find_all():
            if self.canvas.type(item) == 'window':
                self.canvas.itemconfig(item, width=canvas_width)
        for item in self.canvas_.find_all():
            if self.canvas_.type(item) == 'window':
                self.canvas_.itemconfig(item, width=canvas_width)
        for item in self.canvas_lord.find_all():
            if self.canvas_lord.type(item) == 'window':
                self.canvas_lord.itemconfig(item, width=canvas_width)

    def on_mousewheel(self, event):
        x, y = event.x, event.y
        if not self.canvas.find_withtag("text") or not self.canvas.find_overlapping(x, y, x, y):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            self.canvas_.yview_scroll(int(-1 * (event.delta / 120)), "units")
            self.canvas_lord.yview_scroll(int(-1 * (event.delta / 120)), "units")
            pass

    def lord_record(self, root, st, state, username):
        self.canvas_lord.destroy()
        self.scrollbar_lord.destroy()
        self.canvas_lord = tk.Canvas(self.frame_check)
        self.scrollbar_lord = tk.Scrollbar(self.frame_check, orient='vertical', command=self.canvas_lord.yview)
        self.canvas_lord.config(yscrollcommand=self.scrollbar_lord.set)
        self.canvas_lord.grid(row=3, column=0, sticky='nsew')
        self.scrollbar_lord.grid(row=3, column=1, sticky='ns')
        self.canvas_lord.bind('<Configure>', self.on_canvas_resize)
        a = mysql()
        results = a.inquire('users_uplord', 'state', st, state)
        if results:
            for i, row in enumerate(results):
                lorder = str(row[0])
                book_name = str(row[1])
                author_name = str(row[2])
                state = str(row[3])
                if state == 'new':
                    state = '待审核'
                elif state == 'pass':
                    state = '通过'
                elif state == 'fail':
                    state = '不通过'
                button = tk.Button(self.canvas_lord, text='书名:' + book_name + ' 作者:' + author_name + '上传者' + lorder + ' 状态:' + state,
                                   command=lambda book_name = book_name, author_name= author_name, lorder_name = lorder: self.check_select(root, username, book_name, author_name, lorder_name))
                if state != '待审核':
                    button['state'] = 'disabled'
                self.canvas_lord.create_window(0, i * 30, window=button, anchor='nw',
                                               width=self.canvas_lord.winfo_width())
            self.canvas_lord.config(scrollregion=self.canvas_lord.bbox('all'))
        a.close()

    def search_book(self, root, username):
        self.canvas.destroy()
        self.scrollbar.destroy()
        self.canvas = tk.Canvas(self.frame_search_book)
        self.scrollbar = tk.Scrollbar(self.frame_search_book, orient='vertical', command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=1, column=0, sticky='nsew')
        self.scrollbar.grid(row=1, column=1, sticky='ns')
        self.canvas.bind('<Configure>', self.on_canvas_resize)
        value = self.search_e.get()
        a = mysql()
        results = a.search('book_date', 'book_name', 'author_name', value, value)
        if results:
            for i, row in enumerate(results):
                book_name = str(row[0])
                author_name = str(row[1])
                button = tk.Button(self.canvas, text='书名:' + book_name + '   作者:' + author_name+'  上传者:' + str(row[2]), command=lambda book_name = book_name, author_name= author_name:self.book_select(root, username, book_name, author_name))
                self.canvas.create_window(0, i * 30, window=button, anchor='nw', width=self.canvas.winfo_width())
            self.canvas.config(scrollregion=self.canvas.bbox('all'))
            a.close()
        else:
            messagebox.showinfo("提示", "没有找到结果")
            a.close()

    def book_select(self, root, username, book_name, author_name):
        def warning(windows):
            def no():
                tips.destroy()
            def yes():
                a = mysql()
                a.drop(book_name)
                a.delete('book_date', 'book_name', book_name)
                a.close()
                messagebox.showinfo('成功', '《'+book_name+'》'+'删除成功')
                tips.destroy()
                windows.destroy()
            tips = tk.Toplevel()
            tips.title("警告")
            tips.geometry("200x200")
            label = tk.Label(tips, text='删除书籍将会删除书籍的所有信息\n是否还要继续删除该书籍？')
            label.pack()
            button1 = tk.Button(tips, text='   是   ', command=yes)
            button1.pack()
            button2 = tk.Button(tips, text='   否   ', bg='red', command=no)
            button2.pack()
        windows = tk.Toplevel()
        windows.title(book_name)
        windows.geometry('100x50')
        button_view = tk.Button(windows, text='查看', command=lambda: (self.go(root, username, book_name, author_name), windows.destroy()))
        button_view.grid(row=0, column=0, sticky='we')
        button_update = tk.Button(windows, text='修改')
        button_update.grid(row=0, column=1, sticky='we')
        button_delete = tk.Button(windows, text='删除', command=lambda: warning(windows))
        button_delete.grid(row=0, column=2, sticky='we')
        windows.columnconfigure(0, weight=1)
        windows.columnconfigure(1, weight=1)
        windows.columnconfigure(2, weight=1)

    def check_select(self, root, username, book_name, author_name, lorder_name):
        def view():
            win = tk.Toplevel(root)
            win.title('win')
            win.geometry('300x500')
            read.reading(win, username, book_name, author_name)
        def passed():
            a = mysql()
            a.add(book_name, author_name, lorder_name)
            a.update(book_name, 'pass')
            a.close()
            windows.destroy()
        def failed():
            a = mysql()
            a.drop(book_name)
            a.update(book_name, 'fail')
            a.close()
            windows.destroy()

        windows = tk.Toplevel(root)
        windows.title(book_name)
        windows.geometry('100x50')
        button_view = tk.Button(windows, text='查看', command=view)
        button_view.grid(row=0, column=0, sticky='we')
        button_update = tk.Button(windows, text='通过', command=passed)
        button_update.grid(row=0, column=1, sticky='we')
        button_delete = tk.Button(windows, text='不通过', command=failed)
        button_delete.grid(row=0, column=2, sticky='we')
        windows.columnconfigure(0, weight=1)
        windows.columnconfigure(1, weight=1)
        windows.columnconfigure(2, weight=1)

    def search_user(self):
        self.canvas_.destroy()
        self.scrollbar_.destroy()
        self.canvas_ = tk.Canvas(self.frame_search_user)
        self.scrollbar_ = tk.Scrollbar(self.frame_search_user, orient='vertical', command=self.canvas_.yview)
        self.canvas_.config(yscrollcommand=self.scrollbar_.set)
        self.canvas_.grid(row=1, column=0, sticky='nsew')
        self.scrollbar_.grid(row=1, column=1, sticky='ns')
        self.canvas_.bind('<Configure>', self.on_canvas_resize)
        value = self.search_eu.get()
        a = mysql()
        results = a.search('users_date_1', 'username', 'username', value, value)
        if results:
            for i, row in enumerate(results):
                user_name = str(row[0])
                email = str(row[2])
                button = tk.Button(self.canvas_, text='用户名:' + user_name + '   邮箱:' + email, command=lambda user_name = user_name: self.user_select(user_name))
                self.canvas_.create_window(0, i * 30, window=button, anchor='nw', width=self.canvas_.winfo_width())
            self.canvas_.config(scrollregion=self.canvas_.bbox('all'))
            a.close()
        else:
            messagebox.showinfo("提示", "没有找到结果")
            a.close()

    def user_select(self, user_name):
        def warning(windows):
            def no():
                tips.destroy()
            def yes():
                a = mysql()
                a.drop(user_name+'_date')
                a.delete('users_date_1', 'username', user_name)
                a.close()
                messagebox.showinfo('成功', '用户：'+user_name+'删除成功')
                tips.destroy()
                windows.destroy()
            tips = tk.Toplevel()
            tips.title("警告")
            tips.geometry("200x200")
            label = tk.Label(tips, text='删除用户将会删除该用户的所有信息\n是否还要继续删除该用户？')
            label.pack()
            button1 = tk.Button(tips, text='   是   ', command=yes)
            button1.pack()
            button2 = tk.Button(tips, text='   否   ', bg='red', command=no)
            button2.pack()
        windows = tk.Toplevel()
        windows.title(user_name)
        windows.geometry('100x50')
        button_delete = tk.Button(windows, text='删除', command=lambda: warning(windows))
        button_delete.grid(row=0, column=0, sticky='we')
        windows.columnconfigure(0, weight=1)

    def go(self, root, username, bookname, authorname):
        self.frame_search_book.destroy()
        self.frame_mine.destroy()
        self.frame_bottom.destroy()
        self.frame_search_user.destroy()
        self.frame_top.destroy()
        self.frame_check.destroy()
        read.reading(root, username, bookname, authorname)

if __name__ == '__main__':
    root = tk.Tk()
    mainpage(root, 'e-bookadmin')
    root.geometry('300x500')
    root.mainloop()