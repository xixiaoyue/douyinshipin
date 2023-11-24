import asyncio
import threading
import time
import tkinter as tk
from tkinter import filedialog

from config import Config
from douyin import async_http_get, async_batch_http_get


class About(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        tk.Label(self, text="关于作品：本作品由小喵AI制作").pack()
        tk.Label(self, text="关于作者：Thomas").pack()
        tk.Label(self, text="版权所有：小喵AI").pack()
        tk.Label(self, text="首页：直接上传抖音视频分享链接即可").pack()
        tk.Label(self, text="批量：再一个txt文档把抖音分享链接粘贴进去，一行一个，成功后会在text文件夹里").pack()
        tk.Label(self, text="设置：由于语音翻译成文本是由科大讯飞提供，因此需要科大讯飞的appid，secret_key").pack()


class Setting(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        tk.Label(self, text="这是设置页面").grid(row=0,column=0)
        tk.Label(self, text="appid").grid(row=1,column=0)
        self.w1 = tk.Text(self, width=40, height=2)
        self.w1.grid(row=2, column=0)
        tk.Label(self).grid(row=3, column=0)
        tk.Label(self, text="secret_key").grid(row=4, column=0)
        self.w2 = tk.Text(self, width=40, height=2)
        self.w2.grid(row=5, column=0)
        self.Button0 = tk.Button(self,text="确定",command=self.start)
        self.Button0.grid(row=6,column=0)

    def start(self):
        w1_content = self.w1.get(1.0, tk.END)
        w2_content = self.w2.get(1.0, tk.END)
        Config.set_option('config', 'appid', w1_content.strip())
        Config.set_option('config', 'secret_key', w2_content.strip())




class Batch(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        tk.Label(self).grid(row=0,column=0)
        self.w1 = tk.Text(self, width=40, height=2)
        self.w1.grid(row=1, column=0)
        self.Button0 = tk.Button(self, text="选择单个文件",command=self.single_file)
        self.Button0.grid(row=1, column=1)
        tk.Label(self).grid(row=2, column=0)
        self.Button1 = tk.Button(self,text="开始批量操作",command=self.start)
        self.Button1.grid(column=0,row=3)

    def single_file(self):
        file_path = filedialog.askopenfilename()
        self.w1.delete("1.0", tk.END)
        self.w1.insert("insert", file_path)
    def start(self):
        T1 = threading.Thread(name='t1', target=self.event, daemon=True)  # 子线程
        T1.start()
    def event(self):
        l = []
        content = self.w1.get(1.0, tk.END)
        with open(content.strip(), 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line_number, line_content in enumerate(lines, start=1):
                l.append(async_http_get(2,line_content))
            asyncio.run(asyncio.wait(l))



class Home(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        tk.Label(self, text='请输入抖音分享链接').grid(row=0)
        self.douyin_link = tk.Text(self, width=80, height=10)
        self.douyin_link.grid(row=1, column=0)
        tk.Label(self).grid(row=2)
        tk.Label(self, text='翻译的文本').grid(row=3)
        self.douyin_text = tk.Text(self, width=80, height=10)
        self.douyin_text.grid(row=4, column=0)
        tk.Label(self).grid(row=5)
        self.Button0 = tk.Button(self, text="开始", command=self.start)
        self.Button0.grid(row=6, column=0)

    def event(self):
        content = self.douyin_link.get(1.0, tk.END)
        self.Button0["state"] = "disabled"
        self.douyin_text.delete("1.0", tk.END)
        text = asyncio.run(async_http_get(1,content))
        self.clear_text_content()
        self.douyin_text.insert('1.0', text)
        self.Button0["state"] = "normal"


    def start(self):
        T1 = threading.Thread(name='t1', target=self.event, daemon=True)  # 子线程
        T1.start()

    def clear_text_content(self):
        self.douyin_link.delete("1.0", tk.END)
