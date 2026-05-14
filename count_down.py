import tkinter
tim = 120
def foo (button):#倒计时
    global tim
    clock = button.after(1000, lambda: foo(button))
    tim = tim-1
    if tim == 0:
        button['text'] = '再次请求验证码'
        tim = 120
        button.after_cancel(clock)
        button['state'] = 'normal'
    else:
        button['state'] = 'disable'
        button['text'] = str(tim)+'秒后再次请求'

def get (button):
    global tim
    tim = 120
    button.after(1000, lambda: foo(button))

if __name__ == '__main__':
    root = tkinter.Tk()
    but = tkinter.Button(root, text='请求验证码', command=lambda: get(but))
    but.pack()
    root.mainloop()