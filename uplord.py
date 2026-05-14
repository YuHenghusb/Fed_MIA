import os
import pymysql
import chardet
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class mysql():
    def __init__(self):
        self.conn = pymysql.connect(
            host='rm-cn-zpr373ey2000qsoo.rwlb.rds.aliyuncs.com',
            user='e_book',
            password='E-book21xa',
            port=3306,
            database='e_book_date',
            charset='utf8'
        )
        self.cursor = self.conn.cursor()

    def add(self, user_name, book_name, author_name):
        self.cursor.execute("INSERT INTO users_uplord (user_name, book_name, author_name, state) VALUES (%s, %s, %s, 'new')", (user_name, book_name, author_name))
        self.conn.commit()

    def create(self, book_name):
        self.cursor.execute("CREATE TABLE `{}`("
                       "id int auto_increment key,"
                       "page BLOB)".format(book_name))
        self.conn.commit()

    def lord(self, book_name, split_content):
        self.cursor.execute("INSERT INTO `{}` (page) VALUES (%s)".format(book_name), (split_content))
        self.conn.commit()

    def find(self, book_name):
        self.cursor.execute("SELECT * FROM book_date WHERE book_name=%s", (book_name))
        result = self.cursor.fetchone()
        if result == None:
            return 0
        else:
            return 1

    def close(self):
        self.cursor.close()
        self.conn.close()

class run():
    def __init__(self, root, username):
        self.select = tk.Toplevel(root)
        self.select.title("上传书籍")
        self.select.geometry("300x300")
        self.lable_bookname = tk.Label(self.select, text='书名')
        self.lable_bookname.grid(row=1, column=0)
        self.entry_bookname = tk.Entry(self.select)
        self.entry_bookname.grid(row=1, column=1, sticky='we')
        self.lable_authorname = tk.Label(self.select, text='作者')
        self.lable_authorname.grid(row=2, column=0)
        self.entry_authorname = tk.Entry(self.select)
        self.entry_authorname.grid(row=2, column=1, sticky='we')
        self.lable_lord = tk.Label(self.select, text='上传书籍文件')
        self.lable_lord.grid(row=3, columnspan=2)
        self.buttom_lord = tk.Button(self.select, text='选择文件路径', command=self.select_file)
        self.buttom_lord.grid(row=4, column=0)
        self.entry_lord = tk.Entry(self.select)
        self.entry_lord.grid(row=4, column=1, sticky='we')
        self.buttom_ok = tk.Button(self.select, text='上传', command=lambda: self.lording(username))
        self.buttom_ok.grid(row=5, columnspan=2, sticky='we')
        self.select.columnconfigure(1, weight=1)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.entry_lord.delete(0, tk.END)
            self.entry_lord.insert(0, file_path)

    def lording(self, username):
        book_name = self.entry_bookname.get()
        author_name = self.entry_authorname.get()
        file_path = self.entry_lord.get()
        print(book_name, author_name, file_path)
        a = mysql()
        if len(book_name) > 50 or len(author_name) > 50:
            messagebox.showerror('错误', '书名和作者名都不能多于50个字符')
        if a.find(book_name):
            messagebox.showerror('错误', '书库中已经存在同名书籍，请更改书名')
            return
        if file_path.endswith('.txt'):
            try:
                with open(file_path, 'rb') as f:
                    txt_content = f.read()
                    encoding = chardet.detect(txt_content)['encoding']
                    print(encoding)
                    if encoding == 'GB2312' or encoding == 'EUC-JP':
                        encoding = 'ANSI'
                    if encoding == None or encoding == 'None':
                        encoding = 'Windows-1252'
                    txt_content = txt_content.decode(encoding)
            except FileNotFoundError:
                messagebox.showerror('错误', '文件路径不存在')
                a.close()
                return
            except Exception as e:
                print(f"Error: {e}")
                a.close()
                return
            split_size = 3000
            a.add(username, book_name, author_name)
            a.create(book_name)
            split_contents = [txt_content[i:i + split_size] for i in range(0, len(txt_content), split_size)]
            for i, split_content in enumerate(split_contents):
                a.lord(book_name, split_content)
            messagebox.showinfo('上传成功', '请等待管理员审核，审核通过后上架书库')
            a.close()
            self.select.destroy()
            return
        else:
            messagebox.showerror('错误', '文件要为.txt文档')



if __name__ == '__main__':
    root = tk.Tk()
    run(root, 'test123')
    root.geometry('300x500')
    root.mainloop()