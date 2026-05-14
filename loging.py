import tkinter as tk
from tkinter import messagebox
import verify
import count_down
import interface
import pymysql
import bcrypt
import re
import admin_interface

def check_email(email):
    regex = '^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,email)):
        return True
    else:
        return False

class crypt:
    def encrypt(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password
    def verify(self, stored_password, password):
        return bcrypt.checkpw(password.encode(), stored_password.encode())

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
    def search(self, username, password):
        self.cursor.execute("SELECT password FROM users_date_1 WHERE username=%s", username)
        result = self.cursor.fetchone()
        a = crypt()
        if result is None:
            return 0
        elif a.verify(result[0], password):
            return 1
        else:
            return 0
    def inquire(self, value, val):
        self.cursor.execute("SELECT * FROM users_date_1 WHERE {}=%s".format(value), val)
        result = self.cursor.fetchone()
        if result == None:
            return 0
        else:
            return 1

    def up(self):
        self.cursor.execute("SELECT * FROM users_date_1")
        result = self.cursor.fetchone()
        return result[0]

    def find(self, value1, value2, val):
        self.cursor.execute("SELECT {} FROM users_date_1 WHERE {}=%s".format(value1, value2), val)
        result = self.cursor.fetchone()
        return result[0]

    def add(self, username, password, email):
        self.cursor.execute("INSERT INTO users_date_1 (username, password, email) VALUES(%s, %s, %s)", (username, password, email))
        self.cnn.commit()

    def update(self, value, password):
        self.cursor.execute("UPDATE users_date_1 SET `{}`=%s WHERE `email`=%s".format('password'), (password, value))
        self.cnn.commit()

    def create(self, table_name):
        self.cursor.execute("CREATE TABLE {} "
                            "(book_name varchar(50),"
                            "author_name varchar(50),"
                            "record int);".format(table_name))
        self.cnn.commit()

    def close(self):
        self.cursor.close()
        self.cnn.close()


class login:
    def __init__(self, root):
        self.v_code = ''
        self.username =''

        frame_register = tk.Frame(root)  # 注册
        self.Label2 = tk.Label(frame_register, text='注册')
        self.Label2.grid(row=0, columnspan=2)
        self.label_username1 = tk.Label(frame_register, text='用户名')
        self.label_username1.grid(row=1, column=0)
        self.entry_username1 = tk.Entry(frame_register)
        self.entry_username1.grid(row=1, column=1)
        self.label_password1 = tk.Label(frame_register, text='密码')
        self.label_password1.grid(row=2, column=0)
        self.entry_password1 = tk.Entry(frame_register, show='*')
        self.entry_password1.grid(row=2, column=1)
        self.label_password2 = tk.Label(frame_register, text='确认密码')
        self.label_password2.grid(row=3, column=0)
        self.entry_password2 = tk.Entry(frame_register, show='*')
        self.entry_password2.grid(row=3, column=1)
        self.label_email = tk.Label(frame_register, text='邮箱')
        self.label_email.grid(row=4, column=0)
        self.entry_email = tk.Entry(frame_register)
        self.entry_email.grid(row=4, column=1)
        self.entry_vercode = tk.Entry(frame_register)
        self.entry_vercode.grid(row=5, column=0)
        self.v_button = tk.Button(frame_register, text='请求验证码', command=lambda: (self.verify_(self.entry_email.get()), count_down.get(self.v_button)))
        self.v_button.grid(row=5, column=1, sticky='we')
        self.button1 = tk.Button(frame_register, text='注册', command=lambda: self.submit(frame_register, frame_login))
        self.button1.grid(row=6, columnspan=2, sticky='we')
        self.Button4 = tk.Button(frame_register, text='返回', command=lambda:self.change(frame_register,frame_login))
        self.Button4.grid(row=7, columnspan=2, sticky='we')

        frame_login = tk.Frame(root)  # 账号登录
        self.Label1 = tk.Label(frame_login, text='登录')
        self.Label1.grid(row=0, columnspan=2)
        self.label_username = tk.Label(frame_login, text='用户名')
        self.label_username.grid(row=1, column=0)
        self.entry_username = tk.Entry(frame_login)
        self.entry_username.grid(row=1, column=1)
        self.label_password = tk.Label(frame_login, text='密码')
        self.label_password.grid(row=2, column=0)
        self.entry_password = tk.Entry(frame_login, show='*')
        self.entry_password.grid(row=2, column=1)
        self.button_email = tk.Button(frame_login, text='忘记账户或密码？', font=('黑体', 7), command=lambda: self.change(frame_login, frame_forget1))
        self.button_email.grid(row=3, column=1, sticky='e')
        self.Button3 = tk.Button(frame_login, text='登录', command=lambda: self.submit2(root, frame_login))
        self.Button3.grid(row=4, columnspan=2, sticky='we')
        self.Button2 = tk.Button(frame_login, text='注册新用户', command=lambda: self.change(frame_login, frame_register))
        self.Button2.grid(row=5, columnspan=2, sticky='we')
        frame_login.pack(anchor='center')

        frame_forget1 = tk.Frame(root)
        self.title = tk.Label(frame_forget1, text='账户找回')
        self.title.grid(row=0, columnspan=2)
        self.lable = tk.Label(frame_forget1, text='邮箱')
        self.lable.grid(row=1, column=0)
        self.entry_email2 = tk.Entry(frame_forget1)
        self.entry_email2.grid(row=1, column=1)
        self.button2 = tk.Button(frame_forget1, text='查询', command=lambda: self.submit3(frame_forget1, frame_forget2))
        self.button2.grid(row=2, columnspan=2, sticky='we')
        self.Button3 = tk.Button(frame_forget1, text='返回', command=lambda:self.change(frame_forget1,frame_login))
        self.Button3.grid(row=3, columnspan=2, sticky='we')

        frame_forget2 = tk.Frame(root)
        self.title2 = tk.Label(frame_forget2, text='修改密码')
        self.title2.grid(row=0, columnspan=2)
        self.labe = tk.Label(frame_forget2, text='账户名')
        self.labe.grid(row=1, column=0)
        self.user = tk.Label(frame_forget2, text='')
        self.user.grid(row=1, column=1)
        self.label_password_1 = tk.Label(frame_forget2, text='新密码')
        self.label_password_1.grid(row=2, column=0)
        self.entry_password_1 = tk.Entry(frame_forget2, show='*')
        self.entry_password_1.grid(row=2, column=1)
        self.label_password_2 = tk.Label(frame_forget2, text='确认密码')
        self.label_password_2.grid(row=3, column=0)
        self.entry_password_2 = tk.Entry(frame_forget2, show='*')
        self.entry_password_2.grid(row=3, column=1)
        self.email = tk.Label(frame_forget2, text='邮箱')
        self.email.grid(row=4, column=0)
        self.emailshow =tk.Label(frame_forget2, text='')
        self.emailshow.grid(row=4, column=1)
        self.entry_vercode1 = tk.Entry(frame_forget2)
        self.entry_vercode1.grid(row=5, column=0)
        self.v_button1 = tk.Button(frame_forget2, text='请求验证码', command=lambda: (self.verify_(self.emailshow.cget("text")), count_down.get(self.v_button1)))
        self.v_button1.grid(row=5, column=1, sticky='we')
        self.button3 = tk.Button(frame_forget2, text='修改密码', command=lambda:self.submit4(frame_forget2, frame_login))
        self.button3.grid(row=6, columnspan=2, sticky='we')
        self.Button = tk.Button(frame_forget2, text='返回', command=lambda:self.change(frame_forget2, frame_login))
        self.Button.grid(row=7, columnspan=2, sticky='we')

    def change(self, frame1, frame2):
        frame1.pack_forget()
        frame2.pack(anchor='center')

    def submit(self, frame_register, frame_login):
        username = self.entry_username1.get()
        password1 = self.entry_password1.get()
        password2 = self.entry_password2.get()
        email = self.entry_email.get()
        vercode = self.entry_vercode.get()
        a = mysql()
        b = crypt()
        if len(username) == 0:
            messagebox.showerror('错误', '用户名不能为空')
            return
        if len(password1) == 0:
            messagebox.showerror('错误', '密码不能为空')
            return
        if len(username) > 30:
            messagebox.showerror('错误', '输入不得大于30字符')
            return
        if a.inquire('email', email):
            messagebox.showerror('错误', '该邮箱已注册')
            return
        if a.inquire('username', username):
            messagebox.showerror('错误', '用户名已存在')
            return
        if (password1 != password2):
            messagebox.showerror('错误', '前后密码不一致')
            return
        if len(email) == 0:
            messagebox.showerror('错误', '邮箱不能为空')
            return
        if len(vercode) == 0:
            messagebox.showerror('错误', '验证码不能为空')
            return
        if (vercode != self.v_code):
            messagebox.showerror('错误', '验证码错误')
            return
        a.add(username, b.encrypt(password1), email)
        a.create(username+'_date')
        a.close()
        messagebox.showinfo('成功', '注册成功')
        self.change(frame_register, frame_login)

    def verify_(self, email):
        if check_email(email)==False:
            messagebox.showerror('错误', '邮箱格式不合法')
            return
        else:
            self.v_code = verify.get(email)
            return self.v_code

    def submit2(self, root, frame):
        username = self.entry_username.get()
        password = self.entry_password.get()
        a = mysql()
        if a.search(username, password):
            messagebox.showinfo('成功', '登录成功')
            frame.pack_forget()
            if username == a.up():
                a.close()
                admin_interface.mainpage(root, username)
            else:
                a.close()
                interface.mainpage(root, username)
        else:
            a.close()
            messagebox.showerror('错误', '用户名或密码错误')

    def submit3(self, frame1, frame2):
        email = self.entry_email2.get()
        a = mysql()
        if check_email(email)==False:
            messagebox.showerror('错误', '邮箱格式不合法')
            return
        if a.inquire('email', email) == 0:
            messagebox.showerror('错误', '该邮箱未注册过')
            a.close()
            return
        else:
            self.username = a.find('username', 'email', email)
            a.close()
            self.user['text'] = self.username
            self.emailshow['text'] = email
            self.change(frame1, frame2)

    def submit4(self, frame1, frame2):
        password1 = self.entry_password_1.get()
        password2 = self.entry_password_2.get()
        email = self.entry_email.cget('text')
        vercode = self.entry_vercode1.get()
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
        self.change(frame1, frame2)

if __name__ == '__main__':
    root = tk.Tk()
    root.title('电子书阅读平台')
    root.geometry('400x500')
    login(root)
    root.mainloop()