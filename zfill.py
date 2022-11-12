# coding: utf-8

import struct
from Tkinter import *
import time

#------------------GUI基本信息--------------------------
window = Tk()
# 计算机窗口大小  （宽x高）
window.geometry("800x800")
window.maxsize(800, 550)
# 设置计算机title
window.title("图像视频检查")
#----------------------------------------------

#-----------------------进度条----------------------------------
def change_canvas(now,all):
    x = 600*now/float(all)
    percent = str(round((float(now)/all)*100,2))   #保留3位小数的百分比
    canvas.delete(ALL)
    canvas.create_rectangle(0, 0, x, 20, fill='green')
    text_percent.set(percent+'%')
    canvas.update()

canvas = Canvas(
    window,
    width =600,
    height=15,
    # bd =5,
    bg="white"

)
text_percent = StringVar()
text_percent.set('0.00%')
lable = Label(
    window,
    width=5,
    height=2,
    bg="white",
    textvariable=text_percent
)
canvas.pack()
lable.pack()

# 测试函数
i = 0
for i in range(1000) :
    time.sleep(0.01)
    change_canvas(i,1000)
    i +=1


window.mainloop()
