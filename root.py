import tkinter as tk
import loging
flag = 1
username = ''
root = tk.Tk()
root.title('电子书阅读平台')
root.geometry('400x500')
loging.login(root)
root.mainloop()