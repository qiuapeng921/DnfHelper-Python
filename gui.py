"""
本代码由[Tkinter布局助手]生成
当前版本:3.1.2
官网:https://www.pytk.net/tkinter-helper
QQ交流群:788392508
"""
from tkinter import *
from tkinter.ttk import *

app_version = "v1.0.0"


# 自动隐藏滚动条
def scrollbar_autohide(bar, widget):
    def show():
        bar.lift(widget)

    def hide():
        bar.lower(widget)

    hide()
    widget.bind("<Enter>", lambda e: show())
    bar.bind("<Enter>", lambda e: show())
    widget.bind("<Leave>", lambda e: hide())
    bar.bind("<Leave>", lambda e: hide())


class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.dstr = StringVar()

        self.tk_label_card_label = self.__tk_label_card_label()
        self.tk_input_card_edit = self.__tk_input_card_edit()
        self.tk_button_activation = self.__tk_button_activation()
        self.tk_text_edit_content = self.__tk_text_edit_content()
        self.tk_label_run_label = self.__tk_label_run_label()
        self.tk_label_version_label = self.__tk_label_version_label()
        self.tk_label_run_time = self.__tk_label_run_time()
        self.tk_label_app_version = self.__tk_label_app_version()

    def __win(self):
        self.title("DnfHelper-Python")

        # 设置窗口大小、居中
        width = 300
        height = 380
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(False, False)
        self.iconbitmap('./resource/WeGame.ico')

    def __tk_label_card_label(self):
        label = Label(self, text="卡号：", anchor="center")
        label.place(x=0, y=2, width=50, height=30)
        return label

    def __tk_input_card_edit(self):
        ipt = Entry(self, show="*")
        ipt.place(x=50, y=2, width=180, height=30)
        return ipt

    def __tk_button_activation(self):
        btn = Button(self, text="激活")
        btn.place(x=240, y=2, width=50, height=30)
        return btn

    def __tk_text_edit_content(self):
        text = Text(self, font=("微软雅黑", 10))
        text.place(x=2, y=40, width=293, height=320)
        vbar = Scrollbar(self)
        text.configure(yscrollcommand=vbar.set)
        vbar.config(command=text.yview)
        vbar.place(x=280, y=40, width=15, height=320)
        scrollbar_autohide(vbar, text)
        return text

    def __tk_label_run_label(self):
        label = Label(self, text="运行时间：", anchor="center")
        label.place(x=0, y=360, width=70, height=24)
        return label

    def __tk_label_version_label(self):
        label = Label(self, text="版本：", anchor="center")
        label.place(x=210, y=360, width=40, height=24)
        return label

    def __tk_label_run_time(self):
        label = Label(self, text="00:00:00", anchor="center", textvariable=self.dstr)
        label.place(x=60, y=360, width=60, height=24)
        return label

    def __tk_label_app_version(self):
        label = Label(self, text=app_version, anchor="center")
        label.place(x=240, y=360, width=50, height=24)
        return label


class Win(WinGUI):

    def __init__(self):
        super().__init__()
        self.__event_bind()

    @classmethod
    def activation_processing(cls, evt):
        print("<Button>事件未处理", evt)

    def __event_bind(self):
        self.tk_button_activation.bind('<Button>', self.activation_processing)

    def get_time(self):
        pass
        self.dstr.set("1111111111111111")
        self.after(1000, self.get_time())


if __name__ == "__main__":
    win = Win()
    win.get_time()
    win.mainloop()
