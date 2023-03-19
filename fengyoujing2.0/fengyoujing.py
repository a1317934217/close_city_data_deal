# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 13:51:00 2022

@author: ShengyueJiang
"""

import tkinter as tk
from urllib import parse
import tkinter.messagebox as msgbox
import webbrowser
import re

class App:
    
    def __init__(self, width = 500, height = 300):
        self.w = width
        self.h = height
        
        self.title = '风油精影视小助手'
        self.root = tk.Tk(className = self.title)
        
        self.url = tk.StringVar()
        
        self.v = tk.IntVar()
        self.v.set(0)
        
        frame_1 = tk.Frame(self.root)
        frame_2 = tk.Frame(self.root)
        
        gruop = tk.Label(frame_1, text = '播放通道：', padx = 10, pady = 10)
        gruop2 = tk.Label(frame_1, text = '如遇不能播放，请更换其他线路，多试几次！', padx = 30, pady = 10)
        tb = tk.Radiobutton(frame_1, text = '第一通道', variable = self.v, value = 0 , width=10, height=3)
        tb2 = tk.Radiobutton(frame_1, text = '第二通道', variable = self.v, value = 1 , width=10, height=3)
        tb3 = tk.Radiobutton(frame_1, text = '第三通道', variable = self.v, value = 2 , width=10, height=3)
        
        label = tk.Label(frame_2, text = '请输入视频地址：')
        entry = tk.Entry(frame_2, textvariable = self.url, highlightthickness = 1, width = 35)
        button = tk.Button(frame_2, text = '播放', font=('楷体', 12), fg = 'purple', width =2, height = 1, command = self.video_play)
        button_clear = tk.Button(frame_2, text = '清空', font=('楷体', 12), fg = 'purple', width =2, height = 1, command = self.address_clear)
        
        frame_1.pack()
        frame_2.pack()
        
        gruop.grid(row = 0, column = 0)
        tb.grid(row = 0, column = 1)
        tb2.grid(row = 0, column = 2)
        tb3.grid(row = 0, column = 3)
        gruop2.grid(row = 1, columnspan = 4)
        
        label.grid(row = 0, column = 0)
        entry.grid(row = 0, column = 1)
        button.grid(row = 0, column = 2, ipadx = 10, ipady = 2)
        button_clear.grid(row = 0, column = 3, ipadx = 10, ipady = 2)
        
        self.entry = entry
    
    def video_play(self):
        
        port = 'http://www.wmxz.wang/video.php?url='
        port1 = 'https:////jx.playerjy.com/?url='
        port2 = 'http:////jx.m3u8.tv/jiexi/?url='
        if self.v.get() ==0:
            p = port
        elif self.v.get() ==1:
            p = port1
        elif self.v.get() ==2:
            p = port2

        if re.match(r'https?:/{2}\w.+$', self.url.get()):
            ip = self.url.get()
            ip = parse.quote_plus(ip)
            webbrowser.open(p + parse.quote(ip))
        else:
            msgbox.showerror(title='错误', message="视频地址无效")
    
    def address_clear(self):
        self.entry.delete(0, "end")
        
    def loop(self):
        self.root.resizable(True, True)
        self.root.mainloop()
        
app = App()
app.loop()