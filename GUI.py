import tkinter as tk

from view import About, Setting, Batch, Home


class MainPage:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('小喵AI抖音脚本爬取 V1.0.0')
        self.root.geometry('1150x580+450+200')
        self.create_page()
        self.home_frame.pack()

    def create_page(self):
        menubar = tk.Menu(self.root)
        menubar.add_command(label='首页', command=self.show_home)
        menubar.add_command(label='批量', command=self.show_batch)
        menubar.add_command(label='设置', command=self.show_setting)
        menubar.add_command(label='关于', command=self.show_about)
        self.root['menu'] = menubar

        self.about_frame = About(self.root)
        self.setting_frame = Setting(self.root)
        self.batch_frame = Batch(self.root)
        self.home_frame = Home(self.root)

    def show_about(self):
        self.setting_frame.pack_forget()
        self.home_frame.pack_forget()
        self.batch_frame.pack_forget()
        self.about_frame.pack_forget()
        self.about_frame.pack()

    def show_setting(self):
        self.setting_frame.pack_forget()
        self.home_frame.pack_forget()
        self.batch_frame.pack_forget()
        self.about_frame.pack_forget()
        self.setting_frame.pack()

    def show_batch(self):
        self.setting_frame.pack_forget()
        self.home_frame.pack_forget()
        self.batch_frame.pack_forget()
        self.about_frame.pack_forget()
        self.batch_frame.pack()

    def show_home(self):
        self.setting_frame.pack_forget()
        self.home_frame.pack_forget()
        self.batch_frame.pack_forget()
        self.about_frame.pack_forget()
        self.home_frame.pack()


if __name__ == '__main__':
    root = tk.Tk()
    MainPage(root)
    root.mainloop()
