import tkinter as tk
from tkinter import messagebox
import pymysql
import loging
import verify
import count_down
import read
import uplord
import bcrypt

class crypt:
    def encrypt(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password

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

    def record_(self, table):
        self.cursor.execute("SELECT * FROM `{}`".format(table))
        result = self.cursor.fetchall()
        return result

    def found(self, table, column, value, finwhat):
        self.cursor.execute("SELECT `{}` FROM `{}` WHERE `{}` = %s".format(finwhat, table, column), (value))
        result = self.cursor.fetchone()
        return result

    def inquire(self, table, column, value):
        self.cursor.execute("SELECT * FROM `{}` WHERE `{}`=%s".format(table, column), value)
        result = self.cursor.fetchall()
        return result

    def update(self, value, password):
        self.cursor.execute("UPDATE users_date_1 SET `{}`=%s WHERE `email`=%s".format('password'), (password, value))
        self.cnn.commit()

    def drop(self, tablename):
        self.cursor.execute("DROP TABLE `{}`".format(tablename+'_date'))
        self.cnn.commit()

    def delete(self, name):
        self.cursor.execute("DELETE FROM users_date_1 WHERE username=%s", name)
        self.cnn.commit()

    def close(self):
        self.cursor.close()
        self.cnn.close()

class mainpage:
    def __init__(self, root, username):
        self.v_code = ''
        a = mysql()
        email =a.found('users_date_1', 'username', username, 'email')

        self.frame_top = tk.Frame(root, relief='groove')
        self.label = tk.Label(self.frame_top, text='欢迎'+username)
        self.label.pack(side='left')
        self.frame_top.pack(side='top', fill='x')

        self.frame_bottom = tk.Frame(root)
        self.search = tk.Button(self.frame_bottom, relief='raised', text='搜索', command=lambda: self.change(self.frame_search, self.search), state='disabled')
        self.search.grid(row=0, column=0, sticky='ew')
        self.bookrack = tk.Button(self.frame_bottom, relief='raised', text='阅读记录', command=lambda: (self.change(self.frame_record, self.bookrack), self.recording(root, username)))
        self.bookrack.grid(row=0, column=1, sticky='ew')
        self.message = tk.Button(self.frame_bottom, relief='raised', text='上传书籍', command=lambda: (self.change(self.frame_uplord, self.message), self.lord_record(username)))
        self.message.grid(row=0, column=2, sticky='ew')
        self.mine = tk.Button(self.frame_bottom, relief='raised', text='我的', command=lambda: self.change(self.frame_mine, self.mine))
        self.mine.grid(row=0, column=3, sticky='ew')
        self.frame_bottom.columnconfigure(0, weight=1)
        self.frame_bottom.columnconfigure(1, weight=1)
        self.frame_bottom.columnconfigure(2, weight=1)
        self.frame_bottom.columnconfigure(3, weight=1)
        self.frame_bottom.pack(side='bottom', fill='x')

        self.frame_search = tk.Frame(root)
        self.search_e = tk.Entry(self.frame_search)
        self.search_e.grid(row=0, column=0, sticky='new')
        self.search_b = tk.Button(self.frame_search, text='搜索', relief='raised', command=lambda: self.search_book(root, username))
        self.search_b.grid(row=0, column=1, sticky='ne')
        self.canvas = tk.Canvas(self.frame_search)
        self.scrollbar = tk.Scrollbar(self.frame_search, orient='vertical', command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=1, column=0, sticky='nsew')
        self.scrollbar.grid(row=1, column=1, sticky='ns')
        self.canvas.bind('<Configure>', self.on_canvas_resize)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.frame_search.grid_rowconfigure(1, weight=1)
        self.frame_search.grid_columnconfigure(0, weight=1)
        self.frame_search.pack(fill='both', expand=True)

        self.frame_mine = tk.Frame(root)
        self.lable1 = tk.Label(self.frame_mine, text=username, font=('黑体', 15))
        self.lable1.grid(row=0, sticky='we')
        self.lable2 = tk.Label(self.frame_mine, text=email[0], font=('黑体', 7))
        self.lable2.grid(row=1, sticky='we')
        self.updated = tk.Button(self.frame_mine, text='修改密码', command=lambda: self.change_password(username, email[0]))
        self.updated.grid(row=2, sticky='we')
        self.quit = tk.Button(self.frame_mine, text='退出登录', command=lambda: self.quitout(root))
        self.quit.grid(row=3, sticky='we')
        self.cancel = tk.Button(self.frame_mine, text='注销账号', command=lambda: self.cancel_(root, username))
        self.cancel.grid(row=4, sticky='we')
        self.frame_mine.columnconfigure(0, weight=1)

        self.frame_record = tk.Frame(root)
        self.canvas_ = tk.Canvas(self.frame_record)
        self.scrollbar_ = tk.Scrollbar(self.frame_record, orient='vertical', command=self.canvas_.yview)
        self.canvas_.config(yscrollcommand=self.scrollbar_.set)
        self.canvas_.grid(row=1, column=0, sticky='nsew')
        self.scrollbar_.grid(row=1, column=1, sticky='ns')
        self.canvas_.bind('<Configure>', self.on_canvas_resize)
        self.canvas_.bind_all("<MouseWheel>", self.on_mousewheel)
        self.frame_record.grid_rowconfigure(1, weight=1)
        self.frame_record.grid_columnconfigure(0, weight=1)


        self.frame_uplord = tk.Frame(root)
        self.button_lord = tk.Button(self.frame_uplord, text='上传书籍', command=lambda: uplord.run(root, username))
        self.button_lord.grid(row=0, columnspan=2, sticky='we')
        self.lable_lord = tk.Label(self.frame_uplord, text='上传记录及状态')
        self.lable_lord.grid(row=1, columnspan=2, sticky='we')
        self.canvas_lord = tk.Canvas(self.frame_uplord)
        self.scrollbar_lord = tk.Scrollbar(self.frame_uplord, orient='vertical', command=self.canvas_lord.yview)
        self.canvas_lord.config(yscrollcommand=self.scrollbar_lord.set)
        self.canvas_lord.grid(row=2, column=0, sticky='nsew')
        self.scrollbar_lord.grid(row=2, column=1, sticky='ns')
        self.canvas_lord.bind('<Configure>', self.on_canvas_resize)
        self.canvas_lord.bind_all("<MouseWheel>", self.on_mousewheel)
        self.frame_uplord.grid_rowconfigure(2, weight=1)
        self.frame_uplord.grid_columnconfigure(0, weight=1)

        a.close()

    def quitout(self, root):
        self.frame_top.pack_forget()
        self.frame_bottom.pack_forget()
        self.frame_mine.pack_forget()
        self.frame_search.pack_forget()
        loging.login(root)

    def change(self, frame2, button2):
        self.frame_search.pack_forget()
        self.frame_mine.pack_forget()
        self.frame_uplord.pack_forget()
        self.frame_record.pack_forget()
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

    def search_book(self, root, username):
        self.canvas.destroy()
        self.scrollbar.destroy()
        self.canvas = tk.Canvas(self.frame_search)
        self.scrollbar = tk.Scrollbar(self.frame_search, orient='vertical', command=self.canvas.yview)
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
                button = tk.Button(self.canvas, text='书名:' + book_name + '   作者:' + author_name+'  上传者:' + str(row[2]), command=lambda book_name = book_name, author_name = author_name: self.go(root, username, book_name, author_name))
                self.canvas.create_window(0, i * 30, window=button, anchor='nw', width=self.canvas.winfo_width())
            self.canvas.config(scrollregion=self.canvas.bbox('all'))
            a.close()
        else:
            messagebox.showinfo("提示", "没有找到结果")
            a.close()

    def recording(self, root, username):
        a = mysql()
        results = a.record_(username+'_date')
        if results:
            for i, row in enumerate(results):
                book_name = str(row[0])
                author_name = str(row[1])
                button = tk.Button(self.canvas_, text='书名:' + book_name + '   作者:' + author_name + '   读到第' + str(row[2]) + '页', command=lambda book_name = book_name, author_name = author_name: self.go(root, username, book_name, author_name))
                self.canvas_.create_window(0, i * 30, window=button, anchor='nw', width=self.canvas_.winfo_width())
            self.canvas_.config(scrollregion=self.canvas_.bbox('all'))
        a.close()

    def lord_record(self, username):
        self.canvas_lord.destroy()
        self.scrollbar_lord.destroy()
        self.canvas_lord = tk.Canvas(self.frame_uplord)
        self.scrollbar_lord = tk.Scrollbar(self.frame_uplord, orient='vertical', command=self.canvas_lord.yview)
        self.canvas_lord.config(yscrollcommand=self.scrollbar_lord.set)
        self.canvas_lord.grid(row=2, column=0, sticky='nsew')
        self.scrollbar_lord.grid(row=2, column=1, sticky='ns')
        self.canvas_lord.bind('<Configure>', self.on_canvas_resize)
        a = mysql()
        results = a.inquire('users_uplord', 'user_name', username)
        if results:
            for i, row in enumerate(results):
                book_name = str(row[1])
                author_name = str(row[2])
                state = str(row[3])
                if state == 'new':
                    state = '待审核'
                elif state == 'pass':
                    state = '通过'
                elif state == 'fail':
                    state = '不通过'
                button = tk.Button(self.canvas_lord, text='书名:' + book_name + ' 作者:' + author_name + ' 状态:' + state)
                self.canvas_lord.create_window(0, i * 30, window=button, anchor='nw',
                                               width=self.canvas_lord.winfo_width())
            self.canvas_lord.config(scrollregion=self.canvas_lord.bbox('all'))
        a.close()


    def verify_(self, email):
        if loging.check_email(email)==False:
            messagebox.showerror('错误', '邮箱格式不合法')
            return
        else:
            self.v_code = verify.get(email)

    def change_password(self, username, email):
        def change(frame1, frame2):
            frame1.pack_forget()
            frame2.pack()
        def destory():
            tips.destroy()

        def submit4():
            password1 = entry1.get()
            password2 = entry2.get()
            vercode = entcode.get()
            a = mysql()
            b = crypt()
            if (password1 != password2):
                messagebox.showerror('错误', '前后密码不一致')
                return
            if len(vercode) == 0:
                messagebox.showerror('错误', '验证码不能为空')
                return
            if (vercode != self.v_code):
                messagebox.showerror('错误', '验证码错误')
                return
            a.update(email, b.encrypt(password1))
            a.close()
            messagebox.showinfo('成功', '密码修改成功')
            tips.destroy()

        tips = tk.Toplevel()
        tips.title("修改密码")
        tips.geometry("200x200")
        frame_1 = tk.Frame(tips)
        label = tk.Label(frame_1, text='是否确定要修改密码？')
        label.grid(row=0, sticky='ew')
        button1 = tk.Button(frame_1, text='是', bg='green', fg='white', command=lambda: change(frame_1, frame_2))
        button1.grid(row=1, sticky='ew')
        button2 = tk.Button(frame_1, text='否', bg='red', fg='white', command=destory)
        button2.grid(row=2, sticky='ew')
        frame_1.pack()
        frame_2 = tk.Frame(tips)
        lanle1 = tk.Label(frame_2, text='用户名:'+username)
        lanle1.grid(row=0, columnspan=2, sticky='nw')
        lanle2 = tk.Label(frame_2, text='邮箱:'+email)
        lanle2.grid(row=1, columnspan=2, sticky='nw')
        tk.Label(frame_2, text='新密码').grid(row=2, column=0)
        entry1 = tk.Entry(frame_2)
        entry1.grid(row=2, column=1)
        tk.Label(frame_2, text='确认密码').grid(row=3, column=0)
        entry2 = tk.Entry(frame_2)
        entry2.grid(row=3, column=1)
        button1 =tk.Button(frame_2, text='获取验证码', command=lambda: (self.verify_(email), count_down.get(button1)))
        button1.grid(row=4, column=0)
        entcode = tk.Entry(frame_2)
        entcode.grid(row=4, column=1)
        button2 = tk.Button(frame_2, text='修改密码', bg='red', command=submit4)
        button2.grid(row=5, columnspan=2, sticky='we')

    def cancel_(self, root, username):
        def destory():
            tips.destroy()
        def canselall(root, username):
            a = mysql()
            a.drop(username)
            a.delete(username)
            a.close()
            tips.destroy()
            self.quitout(root)
        tips = tk.Toplevel()
        tips.title("警告")
        tips.geometry("200x200")
        label = tk.Label(tips, text='注销账号将会删除所有用户数据\n是否还要继续注销账号？')
        label.pack()
        button1 = tk.Button(tips, text='   是   ', command=lambda: canselall(root, username))
        button1.pack()
        button2 = tk.Button(tips, text='   否   ', bg='red', command=destory)
        button2.pack()

    def go(self, root, username, bookname, authorname):
        self.frame_search.destroy()
        self.frame_mine.destroy()
        self.frame_bottom.destroy()
        self.frame_record.destroy()
        self.frame_top.destroy()
        self.frame_uplord.destroy()
        read.reading(root, username, bookname, authorname)

if __name__ == '__main__':
    root = tk.Tk()
    mainpage(root, 'test123')
    root.geometry('300x500')
    root.mainloop()