import pymysql
import tkinter as tk
import interface
import admin_interface

class mysql():
    def __init__(self):
        self.conn = pymysql.connect(
            host='rm-cn-zpr373ey2000qsoo.rwlb.rds.aliyuncs.com',
            user='e_book',
            password='E-book21xa',
            port=3306,
            database='e_book_date',
            charset='utf8',
        )
        self.cursor = self.conn.cursor()

    def reading(self, bookname):
        self.cursor.execute("SELECT * FROM `{}`".format(bookname))
        results = self.cursor.fetchall()
        return results

    def find(self, username, bookname, authorname):
        self.cursor.execute("SELECT record FROM `{}` WHERE book_name=%s".format(username+'_date'), bookname)
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            self.cursor.execute("INSERT INTO `{}` (book_name, author_name, record) VALUES(%s,%s,1)".format(username+'_date'), (bookname, authorname))
            self.conn.commit()
            return 1

    def update(self, username, bookname, record):
        self.cursor.execute("UPDATE {} SET record=%s WHERE book_name=%s".format(username+'_date'), (record, bookname))
        self.conn.commit()

    def up(self):
        self.cursor.execute("SELECT * FROM users_date_1")
        result = self.cursor.fetchone()
        return result[0]

    def close(self):
        self.cursor.close()
        self.conn.close()

class reading():
    def __init__(self, root, username, bookname, authorname):
        a = mysql()
        self.frame_back = tk.Frame(root)
        self.frame_back.pack(side='top', fill='x')
        self.frame_read = tk.Frame(root)
        self.frame_read.pack(fill='both', expand=True)
        self.frame_turn = tk.Frame(root)
        self.frame_turn.pack(side='bottom', fill='x')

        self.buttom_back = tk.Button(self.frame_back, text='返回', relief='raised', command=lambda: self.back(root, username))
        self.buttom_back.grid(row=0, column=0)
        if root.title() == 'win':
            self.buttom_back.grid_remove()
        self.lable_name = tk.Label(self.frame_back, text=bookname)
        self.lable_name.grid(row=0, column=1)
        self.lable = tk.Label(self.frame_back, text='调整字体大小')
        self.lable.grid(row=0, column=2)
        self.scale = tk.Scale(self.frame_back, from_=10, to=20, orient=tk.HORIZONTAL, command=self.update_font_size)
        self.scale.grid(row=0, column=3)
        self.frame_back.columnconfigure(0, weight=1)
        self.frame_back.columnconfigure(1, weight=1)
        self.frame_back.columnconfigure(2, weight=1)
        self.frame_back.columnconfigure(3, weight=1)

        self.text = tk.Text(self.frame_read)
        self.text.grid(row=0, columnspan=2, sticky='news')
        self.scrollbar = tk.Scrollbar(self.frame_read, command=self.text.yview)
        self.scrollbar.grid(row=0, column=2, sticky='ns')
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.current_row = a.find(username, bookname, authorname)
        self.results = a.reading(bookname)
        self.size = len(self.results)
        result = self.results[self.current_row-1]
        self.record = result[0]
        self.file_data = result[1]
        self.file_data = self.file_data.decode('utf-8')
        self.text.insert(tk.END, self.file_data)
        self.text.config(state='disabled')
        self.frame_read.rowconfigure(0, weight=1)
        self.frame_read.columnconfigure(0, weight=1)

        self.prev_button = tk.Button(self.frame_turn, text='上一页', command=lambda: self.prev(username, bookname))
        self.prev_button.grid(row=1, column=0, sticky='we')
        self.lable = tk.Label(self.frame_turn, text=str(self.current_row) + "/" + str(self.size))
        self.lable.grid(row=1, column=1, sticky='we')
        self.next_button = tk.Button(self.frame_turn, text='下一页', command=lambda: self.next(username, bookname))
        self.next_button.grid(row=1, column=2, sticky='we')
        self.frame_turn.columnconfigure(0, weight=1)
        self.frame_turn.columnconfigure(1, weight=1)
        self.frame_turn.columnconfigure(2, weight=1)
        a.close()

    def update_font_size(self, val):
        self.text.config(font=("TkDefaultFont", int(val)))

    def next(self, username, bookname):
            if self.current_row < self.size:
                self.current_row += 1
                result = self.results[self.current_row-1]
                self.record = result[0]
                file_data = result[1]
                file_data = file_data.decode('utf-8')
                self.text.config(state='normal')
                self.text.delete('1.0', tk.END)
                self.text.insert(tk.END, file_data)
                self.text.config(state='disabled')
                self.lable['text'] = str(self.current_row) + "/" + str(self.size)
                a = mysql()
                a.update(username, bookname, self.record)
                print('+1')
                a.close()

    def prev(self, username, bookname):
            if self.current_row > 1:
                self.current_row -= 1
                result = self.results[self.current_row-1]
                self.record = result[0]
                file_data = result[1]
                file_data = file_data.decode('utf-8')
                self.text.config(state='normal')
                self.text.delete('1.0', tk.END)
                self.text.insert(tk.END, file_data)
                self.text.config(state='disabled')
                self.lable['text'] = str(self.current_row) + "/" + str(self.size)
                a = mysql()
                a.update(username, bookname, self.record)
                print('-1')
                a.close()

    def back(self, root, username):
        self.frame_back.destroy()
        self.frame_read.destroy()
        self.frame_turn.destroy()
        a = mysql()
        if username == a.up():
            a.close()
            admin_interface.mainpage(root, username)
        else:
            a.close()
            interface.mainpage(root, username)

if __name__ == '__main__':
    root = tk.Tk()
    reading(root, 'test123', '堂吉诃德1', '塞万提斯')
    root.geometry('300x500')
    root.mainloop()