# coding=utf-8
from tkinter import *
import cv2
import filetype
import xml.dom.minidom
from tkinter import filedialog
from tkinter.filedialog import askdirectory as tkFileDialog
#import tkFileDialog
import os
import struct
import importlib,sys
importlib.reload(sys)
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

#------------------GUI基本信息--------------------------
window = Tk()
# 计算机窗口大小  （宽x高）
window.geometry("800x800")
window.maxsize(800, 550)
# 设置计算机title
window.title("图像视频检查")
#----------------------------------------------


#---------------Frame布局---------------------------------------
F_show1 = Frame(width=800, height=300, bg='#ddd')
F_show2 = Frame(width=800, height=50, bg='#ddd')
F_show3 = Frame(width=800, height=50, bg='#ddd')
F_show4 = Frame(width=800, height=100, bg='#ddd')
F_show5 = Frame(width=800, height=100, bg='#ddd')
F_canvas = Frame(width=800, height=15,)   #进度条



# 添加到主窗体
F_show1.pack()
F_show2.pack(pady=2)
F_show3.pack(pady=2)
F_canvas.pack(pady=2)
F_show4.pack(pady=2)
F_show5.pack(pady=2)
#--------------------------------------------------------------

#-----------------------进度条----------------------------------
def change_canvas(now,all):
    x = 600*now/float(all)
    percent = str(round((float(now)/all)*100,2))   #保留3位小数的百分比
    canvas.delete(ALL)
    canvas.create_rectangle(0, 0, x, 20, fill='green')
    text_percent.set(percent+'%')
    canvas.update()

canvas = Canvas(
    F_canvas,
    width =600,
    height=15,
    # bd =5,
    bg="white"

)
text_percent = StringVar()
text_percent.set('0.00%')
lable = Label(
    F_canvas,
    width=5,
    height=2,
    bg="white",
    textvariable=text_percent
)
canvas.pack(side = LEFT)
lable.pack(side = RIGHT)

#--------------------F_show1，检测结果--------------------------
#滚动条
s = Scrollbar(F_show1)
s.pack(side=RIGHT,fill=Y)
#多行文本框
T = Text(
    F_show1,
    width = 90,
    height = 18,
    font = 16,
    # spacing1=1,
    # spacing2=5,
    # spacing3=5,
    yscrollcommand = s.set,
    # wrap = 'none'
)
T.pack(
    padx = 10,
    pady = 10,
)
s.config(command = T.yview)
#---------------------------------------------------------------


#-----------------------frame_show2，图像/视频文件夹路径----------------------------
#单行文本框,图像/视频文件夹
E1 = Entry(
    F_show2,
    bd =5,
    width=65,
)
E1.pack(side = LEFT)
#-----------------------frame_show2，图像/视频文件夹选择按钮----------------------------
#选择文件夹函数
def b_select_img_dir():
    E1.delete(0,END)
    # default_dir = '‪C:\\Users\\曹成辰\\Desktop\\testpicture1'
    #default_dir = 'C:\\'  # 默认打开路径
    # 返回文件夹路径
    #dirPath = tkFileDialog.askdirectory(title='选择图像/视频文件夹', initialdir=default_dir)
    #dirPath = tkFileDialog().askdirectory(title='选择图像/视频文件夹', initialdir=default_dir)

    dirPath = filedialog.askdirectory(title='选择图像/视频文件夹', initialdir=r'.\video_tzx')

    # dirPath = tkFileDialog().askdirectory(title='选择图像/视频文件夹', initialdir=default_dir)
    E1.insert(0,dirPath)
#选择文件夹按钮
b_select_dir=Button(
    F_show2,
    text="选择图像/视频文件夹",
    width=20,
    height=1,
    activebackground='lightblue',
    font=12,
    bd=3,
    command=b_select_img_dir
)
b_select_dir.pack(side = RIGHT)
#--------------------------------------------------------------------------

#-----------------------frame_show3，标签文件夹路径----------------------------
#单行文本框,标签文件夹
E2 = Entry(
    F_show3,
    bd =5,
    width=65,
)
E2.pack(side = LEFT)
#-----------------------frame_show3，标签文件夹选择按钮----------------------------
#选择标签文件夹函数
def b_select_xml_dir():
    E2.delete(0,END)
    default_dir = 'C:\\'  # 默认打开路径
    # 返回文件夹路径
    #dirPath = tkFileDialog.askdirectory(title='选择标签文件夹', initialdir=default_dir)

    dirPath = filedialog.askdirectory(title='选择标签文件夹',
                                      initialdir=r'.\video_tzx')

    # dirPath = tkFileDialog().askdirectory(title='选择标签文件夹', initialdir=default_dir)
    E2.insert(0,dirPath)
#选择文件夹按钮
b_select_dir=Button(
    F_show3,
    text="选择标签文件夹",
    width=20,
    height=1,
    activebackground='lightblue',
    font=12,
    bd=3,
    command=b_select_xml_dir
)
b_select_dir.pack(side = RIGHT)
#--------------------------------判断文件格式辅助函数------------------------------------------

#-----------------------frame_show4，图像类按钮---------------------------
# 图像检查函数
def check_bmp():
    T.insert(END,'开始检查文件格式是否为bmp,分辨率800*600，位深为8，第一行像素值是否对应文件名.........')
    # 判断是否选择文件夹
    if E1.get() == '':
        T.insert(END,'\n抱歉，您未选择任何文件夹 \n检查完毕。')
        return
    dir_path = E1.get()     #获取待检测文件夹路径
    file_number = 0     #记录文件夹下的文件数量
    file_all = 0    #总文件数 进度条的all
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            file_all += 1
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            file_number += 1
            filePath = os.path.join(root, name) #图片路径
            file_type = 'unknown'

            kind = filetype.guess(filePath)     #图片格式
            if kind is not None:
                file_type = kind.extension
            # file_type = filetype(filePath)   # 读取头文件看文件格式
            # 判断BMP
            if file_type == 'bmp':
                bmp = open(filePath, 'rb')
                # bmp文件头
                bmp.read(2)  #type
                bmp.read(4)  #Size
                bmp.read(2)  #Reserved1
                bmp.read(2)  #Reserved2
                bmp.read(4)  #Offset
                # 位图信息
                bmp.read(4)  #DIB Header Size
                #元组类型宽高
                width = struct.unpack('I', bmp.read(4))
                height = struct.unpack('I', bmp.read(4))

                bmp.read(2)  #Colour Planes
                #元组类型位深
                bits_per_pixel = struct.unpack('H', bmp.read(2))
                # 判断宽，高，位深
                w = width[0]
                h = height[0]
                d = bits_per_pixel[0]
                # bmp.read(1048)      #继续读取1048到达位图像素数据（1048+30）
                # first_line = struct.unpack('I', bmp.read(4)) #int类型10进制
                # print first_line
                # 判断第一行与文件名比对
                # filePath = filePath.replace("/","\")
                gray = cv2.imread(filePath,cv2.IMREAD_GRAYSCALE)     # 读入灰度图
                first_line4 = ""
                for i in range(4):
                    # value = gray[0][i]
                    if gray[0][i] < 10:
                        first_line4 = first_line4 + "0" + str(gray[0][i])
                    elif gray[0][i] == 0:
                        first_line4 = first_line4 + "00"
                    else:
                        first_line4 = first_line4 + str(gray[0][i])
                # hex_first_line = str(hex(first_line[0])) #转16进制,再转字符串为了比较
                # hex_tem = hex_first_line[2:10]  #截取8位有用信息
                n = name.split('.',1)[0]    #截取文件名(文件名-11223344)
                #小端处理方式
                # f = first_line4.decode('hex')[::-1].encode('hex_codec') #第一行的四个字节（11223344）
                # print n
                # print f
                if w==800 and h==600 and d==8 and n==first_line4 :
                    # 继续读取下个文件
                    change_canvas(file_number,file_all)
                    pass
                else:
                    T.insert(END,'\n图片：“' + name + '” 分辨率为:'+str(w)+'x'+str(h)+'，位深为:'+str(d)
                             +',像素第一行前四个字节为：'+first_line4)
                    change_canvas(file_number, file_all)
                bmp.close()  # 关闭文件（重要）
            else:
                #在检测输出框里输出信息
                T.insert(END,'\n文件：“' + name + '” 格式不为bmp。')
                change_canvas(file_number, file_all)
    T.insert(END, '\n检查完毕。\n文件夹：'+E1.get()+'，共有'+str(file_number)+'个文件。')
# 图像检查按钮组件
b_check_img=Button(
    F_show4,
    text="图像检查",
    width=20,
    height=2,
    activebackground='lightblue',
    font=12,
    bd=3,
    command=check_bmp,
)
b_check_img.pack(side = LEFT)
#------------------------------图像是否有对应标签按钮-------------------------
# 图像是否有对应标签函数
def img_tag_cmp():
    T.insert(END, '开始检查每个图像是否有对应标签.........')
    # 判断是否选择文件夹
    if E1.get() == '' or E2.get()== '':
        T.insert(END, '\n抱歉，您未选择图像文件夹或者标签文件夹 \n检查完毕。')
        return
    dir_img_path = E1.get()  # 获取图像文件夹路径
    dir_tag_path = E2.get()  # 获取标签文件夹路径
    file_img_number = 0  # 记录图像文件夹下的文件数量
    file_tag_number = 0  # 记录标签文件夹下的文件数量
    dictionary = {}
    file_all = 0
    #统计所有图片数量
    for img_root, img_dirs, imgs in os.walk(dir_img_path, topdown=False):
        for img_name in imgs:
            file_all +=1
    #统计所有标签数量
    for tag_root, tag_dirs, tags in os.walk(dir_tag_path, topdown=False):
        for tag_name in tags:
            file_tag_number +=1
    #-------------简化方案-----------------------------------------
    for img_name in os.listdir(dir_img_path) :
        dictionary[img_name] = 0
        file_img_number += 1
        for tag_name in os.listdir(dir_tag_path):
            i_n = img_name.split('.', 1)[0]
            t_n = tag_name.split('.', 1)[0]
            if i_n == t_n :
                dictionary[img_name] = 1
                break
        if dictionary[img_name]==1 :
            change_canvas(file_img_number, file_all)
        else:
            T.insert(END, '\n文件：“' + img_name + '”未找到对应标签文件')
            change_canvas(file_img_number, file_all)

    #------------------------------原方案-----------------------------------
    # for img_root, img_dirs, imgs in os.walk(dir_img_path, topdown=False):
    #     # 遍历图片文件夹
    #     for img_name in imgs:
    #         dictionary[img_name] = 0
    #         file_img_number +=1
    #         for tag_root, tag_dirs, tags in os.walk(dir_tag_path, topdown=False):
    #             # 遍历标签文件夹
    #             for tag_name in tags:
    #                 # file_tag_number += 1
    #                 i_n = img_name.split('.', 1)[0]
    #                 t_n = tag_name.split('.', 1)[0]
    #                 if i_n == t_n :
    #                     dictionary[img_name] = 1
    #                     break
    #             if dictionary[img_name]==1 :
    #                 change_canvas(file_img_number, file_all)
    #             else:
    #                 T.insert(END, '\n文件：“' + img_name + '”未找到对应标签文件')
    #                 change_canvas(file_img_number, file_all)
    #----------------------------------------------------------------------------
    # file_tag_number = file_tag_number/file_img_number   #真正的标签文件数量
    # file_img_number = 0
    # for img_root, img_dirs, imgs in os.walk(dir_img_path, topdown=False):
    #     # 遍历图片文件夹
    #     for img_name in imgs:
    #         # 输出没有对应标签的图片
    #         file_img_number +=1
    #         if dictionary[img_name] == 0:
    #             T.insert(END, '\n文件：“'+ img_name +'”未找到对应标签文件')
    #         change_canvas(file_img_number,file_all)
    T.insert(END,'\n检查完毕。\n文件夹：'+E1.get()+'，共有'+str(file_img_number)+'个文件')
    T.insert(END, '\n文件夹：' + E2.get() + '，共有' + str(file_tag_number) + '个文件')
# 图像是否有对应标签按钮： 检查图像文件夹是否都有对应的标签文件
b_img_tag_cmp=Button(
    F_show4,
    text="图像是否有对应标签",
    width=20,
    height=2,
    activebackground='lightblue',
    font=12,
    bd=3,
    command = img_tag_cmp
)
b_img_tag_cmp.pack(side = LEFT)
#--------------------------------图像标签检查----------------------------------
# 检查标签文件是否都有类型，左上坐标，右下坐标，且类型属于统一标准的7类
def check_img_tag():
    T.insert(END, '开始检查标签文件是否都有类型，左上坐标，右下坐标，且类型属于统一标准的7类.........')
    # 判断是否选择文件夹
    if E2.get() == '':
        T.insert(END, '\n抱歉，您未选择任何文件夹 \n检查完毕。')
        return
    tag_dir_path = E2.get()  # 获取待检测文件夹路径
    file_number = 0  # 记录文件夹下的文件数量
    file_all = 0
    for tag_root, tag_dirs, tags in os.walk(tag_dir_path, topdown=False):
        # 遍历图片文件夹
        for tag_name in tags:
            file_all+= 1
    for tag_root, tag_dirs, tags in os.walk(tag_dir_path, topdown=False):
        # 遍历图片文件夹
        for tag_name in tags:
            file_number += 1
            # 打开xml文档
            # print '------------' + tag_name + '---------------------------'
            filePath = os.path.join(tag_root, tag_name)
            dom1 = xml.dom.minidom.parse(filePath)
            # 得到文档元素对象
            root = dom1.documentElement
            # 得到所有name标签,左上坐标，右下坐标
            name_list = root.getElementsByTagName('name')
            xmin_list = root.getElementsByTagName('xmin')
            ymin_list = root.getElementsByTagName('ymin')
            xmax_list = root.getElementsByTagName('xmax')
            ymax_list = root.getElementsByTagName('ymax')
            # 记录个数
            name_len = len(name_list)
            xmin_len = len(xmin_list)
            xmax_len = len(xmax_list)
            ymin_len = len(ymin_list)
            ymax_len = len(ymax_list)
            # 判断都有每个标签
            if name_len == 0 or xmin_len == 0 or xmax_len == 0 or ymin_len == 0 or ymax_len == 0:
                # print '文件“' + tag_name + '”类型或左上坐标或右下坐标缺失'
                T.insert(END,'\n文件“' + tag_name + '”类型或左上坐标或右下坐标缺失')
                change_canvas(file_number,file_all)
                continue
            # 判断每个标签数量需要相同
            elif name_len != xmin_len or xmin_len != xmax_len or xmax_len != ymin_len or ymin_len != ymax_len:
                # print '文件“' + tag_name + '”类型或左上坐标或右下坐标缺失'
                T.insert(END, '\n文件“' + tag_name + '”类型或左上坐标或右下坐标缺失')
                change_canvas(file_number, file_all)
                continue
            # 到达了else说明xml文件都有类型，左上坐标和右下坐标，且对应
            else:
                for type_tag in name_list:
                    tn = type_tag.firstChild.data  # 获取标签内数据 tn->type_name
                    if tn != 'plane' and tn != 'runway' and tn != 'airport_oil_depot' and tn != 'vulcans' and tn != 'radar_vehicle' and tn != 'bridge' and tn != 'ship':
                        # print '文件“' + tag_name + '”检测结果类型不符合统一标准'c
                        T.insert(END, '\n文件“' + tag_name + '”检测结果类型不符合统一的7类标准')
                        break
                change_canvas(file_number, file_all)
    T.insert(END, '\n检查完毕。\n文件夹：'+E2.get()+'，共有'+str(file_number)+'个文件。')
# 图像标签检查按钮组件
b_check_img_tag=Button(
    F_show4,
    text="图像标签检查",
    width=20,
    height=2,
    activebackground='lightblue',
    font=12,
    bd=3,
    command = check_img_tag
)
b_check_img_tag.pack(side = LEFT)
#-----------------------------小目标检查---------------------
# 小目标检查
def check_small_tar():
    T.insert(END, '开始统计七类目标图像数量，以及飞机，地空导弹车，地/海面防空雷达车类小目标图像数量.........')
    # 判断是否选择文件夹
    if E2.get() == '':
        T.insert(END, '\n抱歉，您未选择标签文件夹 \n检查完毕。')
        return
    tag_dir_path = E2.get()  # 获取待检测文件夹路径
    file_number = 0  # 记录文件夹下的文件数量
    file_all = 0
    #--七类--
    plane_number = 0
    runway_number = 0
    airportOilDepot_number = 0
    vulcans_number = 0
    radarVehicle_number = 0
    bridge_number = 0
    ship_number = 0
    # --三类小目标--
    small_plane = 0     #记录飞机类小目标图像数
    small_vulcans = 0   #记录地空导弹车小目标图像数
    small_radar_vehicle = 0     #记录地/海面防空雷达车小目标图像数
    #先记录文件总数用于进度条
    for tag_root, tag_dirs, tags in os.walk(tag_dir_path, topdown=False):
        for tag_name in tags:
            file_all += 1
    file_all *= 10
    # --------------------计算飞机类图像数--------------
    for tag_root, tag_dirs, tags in os.walk(tag_dir_path, topdown=False):
        # 遍历图片文件夹
        for tag_name in tags:
            file_number+=1
            # 打开xml文档
            # print '------------' + tag_name + '---------------------------'
            filePath = os.path.join(tag_root, tag_name)
            dom = xml.dom.minidom.parse(filePath)
            # 得到文档元素对象
            root = dom.documentElement
            # 得到所有name标签
            name_list = root.getElementsByTagName('name')
            # 寻找小飞机目标
            for type_name in name_list:
                tn = type_name.firstChild.data  #记录name标签内的数据
                if tn == 'plane' :
                    #如果找到了一个飞机目标，就找到了一个飞机目标类的图像，无需往下遍历，跳出循环
                    plane_number += 1
                    break
            change_canvas(file_number,file_all)
    # --------------------计算机场跑道类图像数--------------
    for tag_root, tag_dirs, tags in os.walk(tag_dir_path, topdown=False):
        # 遍历图片文件夹
        for tag_name in tags:
            file_number+=1
            # 打开xml文档
            # print '------------' + tag_name + '---------------------------'
            filePath = os.path.join(tag_root, tag_name)
            dom = xml.dom.minidom.parse(filePath)
            # 得到文档元素对象
            root = dom.documentElement
            # 得到所有name标签
            name_list = root.getElementsByTagName('name')
            # 寻找小飞机目标
            for type_name in name_list:
                tn = type_name.firstChild.data  #记录name标签内的数据
                if tn == 'runway' :
                    runway_number += 1
                    break
            change_canvas(file_number,file_all)
    # --------------------计算机场油库类图像数--------------
    for tag_root, tag_dirs, tags in os.walk(tag_dir_path, topdown=False):
        # 遍历图片文件夹
        for tag_name in tags:
            file_number+=1
            # 打开xml文档
            # print '------------' + tag_name + '---------------------------'
            filePath = os.path.join(tag_root, tag_name)
            dom = xml.dom.minidom.parse(filePath)
            # 得到文档元素对象
            root = dom.documentElement
            # 得到所有name标签
            name_list = root.getElementsByTagName('name')
            # 寻找小飞机目标
            for type_name in name_list:
                tn = type_name.firstChild.data  #记录name标签内的数据
                if tn == 'airport_oil_depot' :
                    #如果找到了一个飞机目标，就找到了一个飞机目标类的图像，无需往下遍历，跳出循环
                    airportOilDepot_number += 1
                    break
            change_canvas(file_number, file_all)
    # --------------------计算地空导弹车类图像数--------------
    for tag_root, tag_dirs, tags in os.walk(tag_dir_path, topdown=False):
        # 遍历图片文件夹
        for tag_name in tags:
            file_number+=1
            # 打开xml文档
            # print '------------' + tag_name + '---------------------------'
            filePath = os.path.join(tag_root, tag_name)
            dom = xml.dom.minidom.parse(filePath)
            # 得到文档元素对象
            root = dom.documentElement
            # 得到所有name标签
            name_list = root.getElementsByTagName('name')
            # 寻找小飞机目标
            for type_name in name_list:
                tn = type_name.firstChild.data  #记录name标签内的数据
                if tn == 'vulcans' :
                    vulcans_number += 1
                    break
            change_canvas(file_number, file_all)
    # --------------------计算雷达车类图像数--------------
    for tag_root, tag_dirs, tags in os.walk(tag_dir_path, topdown=False):
        # 遍历图片文件夹
        for tag_name in tags:
            file_number+=1
            # 打开xml文档
            # print '------------' + tag_name + '---------------------------'
            filePath = os.path.join(tag_root, tag_name)
            dom = xml.dom.minidom.parse(filePath)
            # 得到文档元素对象
            root = dom.documentElement
            # 得到所有name标签
            name_list = root.getElementsByTagName('name')
            # 寻找小飞机目标
            for type_name in name_list:
                tn = type_name.firstChild.data  #记录name标签内的数据
                if tn == 'radar_vehicle' :
                    radarVehicle_number += 1
                    break
            change_canvas(file_number, file_all)
    # --------------------计算桥梁类图像数--------------
    for tag_root, tag_dirs, tags in os.walk(tag_dir_path, topdown=False):
        # 遍历图片文件夹
        for tag_name in tags:
            file_number+=1
            # 打开xml文档
            # print '------------' + tag_name + '---------------------------'
            filePath = os.path.join(tag_root, tag_name)
            dom = xml.dom.minidom.parse(filePath)
            # 得到文档元素对象
            root = dom.documentElement
            # 得到所有name标签
            name_list = root.getElementsByTagName('name')
            # 寻找小飞机目标
            for type_name in name_list:
                tn = type_name.firstChild.data  #记录name标签内的数据
                if tn == 'bridge' :
                    bridge_number += 1
                    break
            change_canvas(file_number, file_all)
    # --------------------计算运输舰艇类图像数--------------
    for tag_root, tag_dirs, tags in os.walk(tag_dir_path, topdown=False):
        # 遍历图片文件夹
        for tag_name in tags:
            file_number+=1
            # 打开xml文档
            # print '------------' + tag_name + '---------------------------'
            filePath = os.path.join(tag_root, tag_name)
            dom = xml.dom.minidom.parse(filePath)
            # 得到文档元素对象
            root = dom.documentElement
            # 得到所有name标签
            name_list = root.getElementsByTagName('name')
            # 寻找小飞机目标
            for type_name in name_list:
                tn = type_name.firstChild.data  #记录name标签内的数据
                if tn == 'ship' :
                    ship_number += 1
                    break
            change_canvas(file_number, file_all)
    # --------------------计算飞机类小目标图像数--------------
    for tag_root, tag_dirs, tags in os.walk(tag_dir_path, topdown=False):
        # 遍历图片文件夹
        for tag_name in tags:
            file_number+=1
            # 打开xml文档
            # print '------------' + tag_name + '---------------------------'
            filePath = os.path.join(tag_root, tag_name)
            dom = xml.dom.minidom.parse(filePath)
            # 得到文档元素对象
            root = dom.documentElement
            # 得到所有name标签,左上坐标，右下坐标
            name_list = root.getElementsByTagName('category')
            xmin_list = root.getElementsByTagName('xmin')
            ymin_list = root.getElementsByTagName('ymin')
            xmax_list = root.getElementsByTagName('xmax')
            ymax_list = root.getElementsByTagName('ymax')
            # 寻找小飞机目标
            for i,type_name in enumerate(name_list):
                tn = type_name.firstChild.data  #记录name标签内的数据
                # 记录此目标 像素宽高
                width = int(xmax_list[i].firstChild.data) - int(xmin_list[i].firstChild.data)
                height = int(ymax_list[i].firstChild.data) - int(ymin_list[i].firstChild.data)
                area = width*height
                if tn == 'plane' and area >= 92.16 and area <= 256:
                    #如果找到了一个小飞机目标，就找到了一个小飞机目标类的图像，无需往下遍历，跳出循环
                    small_plane += 1
                    break
            change_canvas(file_number, file_all)
    # --------------------计算地空导弹车类小目标图像数--------------
    for tag_root, tag_dirs, tags in os.walk(tag_dir_path, topdown=False):
        # 遍历图片文件夹
        for tag_name in tags:
            file_number+=1
            # 打开xml文档
            # print '------------' + tag_name + '---------------------------'
            filePath = os.path.join(tag_root, tag_name)
            dom = xml.dom.minidom.parse(filePath)
            # 得到文档元素对象
            root = dom.documentElement
            # 得到所有name标签,左上坐标，右下坐标
            name_list = root.getElementsByTagName('name')
            xmin_list = root.getElementsByTagName('xmin')
            ymin_list = root.getElementsByTagName('ymin')
            xmax_list = root.getElementsByTagName('xmax')
            ymax_list = root.getElementsByTagName('ymax')
            # 寻找小飞机目标
            for i,type_name in enumerate(name_list):
                tn = type_name.firstChild.data  #记录name标签内的数据
                # 记录此目标 像素宽高
                width = int(xmax_list[i].firstChild.data) - int(xmin_list[i].firstChild.data)
                height = int(ymax_list[i].firstChild.data) - int(ymin_list[i].firstChild.data)
                area = width*height
                if tn == 'vulcans' and  area >= 92.16 and area <= 256:
                    #如果找到了一个地空导弹车小目标，就找到了一个地空导弹车小目标类的图像，无需往下遍历，跳出循环
                    small_vulcans += 1
                    break
            change_canvas(file_number, file_all)
    # --------------------计算地/海面防空雷达车小目标图像数--------------
    for tag_root, tag_dirs, tags in os.walk(tag_dir_path, topdown=False):
        # 遍历图片文件夹
        for tag_name in tags:
            file_number += 1
            # 打开xml文档
            # print '------------' + tag_name + '---------------------------'
            filePath = os.path.join(tag_root, tag_name)
            dom = xml.dom.minidom.parse(filePath)
            # 得到文档元素对象
            root = dom.documentElement
            # 得到所有name标签,左上坐标，右下坐标
            name_list = root.getElementsByTagName('name')
            xmin_list = root.getElementsByTagName('xmin')
            ymin_list = root.getElementsByTagName('ymin')
            xmax_list = root.getElementsByTagName('xmax')
            ymax_list = root.getElementsByTagName('ymax')
            # 寻找小飞机目标
            for i, type_name in enumerate(name_list):
                tn = type_name.firstChild.data  # 记录name标签内的数据
                # 记录此目标 像素宽高
                width = int(xmax_list[i].firstChild.data) - int(xmin_list[i].firstChild.data)
                height = int(ymax_list[i].firstChild.data) - int(ymin_list[i].firstChild.data)
                area = width*height
                if tn == 'radar_vehicle' and area >= 92.16 and area <= 256:
                    # 如果找到了一个地/海面防空雷达车小目标，就找到了一个地/海面防空雷达车小目标类的图像，无需往下遍历，跳出循环
                    small_radar_vehicle += 1
                    break
            change_canvas(file_number,file_all)
    # 七类目标图像数
    T.insert(END,'\n\n统计七类目标图像数量如下：')
    T.insert(END, '\n"飞机"类目标图像共有“' + str(plane_number) + '”张')
    T.insert(END, '\n"机场跑道"类目标图像共有“' + str(runway_number) + '”张')
    T.insert(END, '\n"机场油库"类目标图像共有“' + str(airportOilDepot_number) + '”张')
    T.insert(END, '\n"地空导弹车"类目标图像共有“' + str(vulcans_number) + '”张')
    T.insert(END, '\n"地/海面防空雷达车"类目标图像共有“' + str(radarVehicle_number) + '”张')
    T.insert(END, '\n"桥梁"类目标图像共有“' + str(bridge_number) + '”张')
    T.insert(END, '\n"运输舰艇"类目标图像共有“' + str(ship_number) + '”张')
    # 三类小目标图像数
    T.insert(END, '\n\n统计三类小目标图像数量如下：')
    T.insert(END, '\n"飞机"类小目标图像共有“'+str(small_plane)+'”张')
    T.insert(END, '\n"地空导弹车"类小目标图像共有“'+str(small_vulcans)+'”张')
    T.insert(END, '\n"地/海面防空雷达车"类小目标图像共有“'+str(small_radar_vehicle)+'”张')
    # 求得5%数量
    T.insert(END,'\n\n判别三类小目标数量是否达到该类的5%：')
    T.insert(END, '\n"飞机"类图像数的5%有“' + str(plane_number*0.05) + '”张')
    T.insert(END, '\n"地空导弹车"类图像数的5%有“' + str(vulcans_number*0.05) + '”张')
    T.insert(END, '\n"地/海面防空雷达车"类图像数的5%有“' + str(radarVehicle_number*0.05) + '”张')
    # 判断5%以上
    if  small_plane < plane_number * 0.05 :
        T.insert(END, '\n“飞机”类小目标图像数量没有达到此类图像数的5%以上')
    if  small_vulcans < vulcans_number * 0.05 :
        T.insert(END, '\n“地空导弹车”类小目标图像数量没有达到此类图像数的5%以上')
    if  small_radar_vehicle < radarVehicle_number * 0.05 :
        T.insert(END, '\n“地/海面防空雷达车”类小目标图像数量没有达到此类图像数的5%以上')
    T.insert(END,'\n\n检查完毕。')
    T.insert(END,'\n文件夹下共有“'+str(file_number/10)+'”个文件')
# 小目标检查按钮组件
b_check_img_tag=Button(
    F_show4,
    text="小目标检查",
    width=20,
    height=2,
    activebackground='lightblue',
    font=12,
    bd=3,
    command = check_small_tar
)
b_check_img_tag.pack(side = LEFT)
#-----------------------frame_show5，视频类按钮+复位---------------------------
#-----------------------------视频检查------------------------
# 检查视频文件夹下所有视频是否是avi格式，每帧分辨率800*600，帧频30fps，位深8，帧数>900
def check_avi():
    T.insert(END, '开始检查视频是否是avi格式，是否有帧损，分辨率800*600，帧频30fps，帧数不低于900,每帧第一行是否包含对应帧号.........')
    # 判断是否选择文件夹
    if E1.get() == '':
        T.insert(END, '\n抱歉，您未选择任何文件夹 \n检查完毕。')
        return
    dir_path = E1.get()  # 获取待检测文件夹路径
    file_number = 0  # 记录文件夹下的文件数量
    file_all = 0
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            file_all += 1
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            file_number += 1
            filePath = os.path.join(root, name)  # 视频路径
            file_type = 'unknown'
            kind = filetype.guess(filePath)
            if kind is not None:
                file_type = kind.extension
            if file_type != 'avi':
                T.insert(END, '\n文件：“' + name + '” 格式不为avi')
                change_canvas(file_number,file_all)
                continue
            # 读头文件看位深
            # avi = open(filePath, 'rb')
            # #跳过186字节
            # avi.read(186)
            # # 元组类型位深
            # bits_per_pixel = struct.unpack('H', avi.read(2))
            # deep = bits_per_pixel[0]
            # avi.close()
            # if int(deep)!=8:
            #     T.insert(END, '\n文件：“' + name + '” 检测的位深为：“' + str(deep) + '”,帧位深不为8')
            #     change_canvas(file_number, file_all)
            #     continue
            video_cap = cv2.VideoCapture(filePath)  #读视频
            if video_cap.isOpened() == False:
                T.insert(END, '\n文件：“' + name + '” 读取失败')
                change_canvas(file_number, file_all)
                continue
            #读取成功
            # print video_cap.get(3)  # 视频宽
            # print video_cap.get(4)  # 视频高
            vn = video_cap.get(7)  # 帧数
            # T.insert(END, '\n帧数：“' + str(video_frame_number ))
            video_frame_number = 0          #帧数
            video_fps = video_cap.get(5)    # 帧率
            # 求得帧数，每帧分辨率
            while (True):
                ret, frame = video_cap.read()
                if ret is False:
                    break
                video_frame_number += 1
                # 取得宽，高，判断每个像素的3个通道是否一样以此判断位深为8
                height = frame.shape[0]
                width = frame.shape[1]
                #检查每个像素的三通道 480000次
                # for row in range(height):
                #     for colum in range(width):
                #         if frame[height - 1][colum - 1][0] == frame[height - 1][colum - 1][1] == \
                #                 frame[height - 1][colum - 1][2]:
                #             continue
                #         else:
                #             T.insert(END, '\n文件：“' + name + '” 的第“' + str(video_frame_number) + '”帧位深不为8')
                #             break   #不是八位位深则直接检查下个视频

                # 检查第一行像素的三通道 800次
                # for colum in range(width):
                #     if frame[0][colum - 1][0] == frame[0][colum - 1][1] == \
                #             frame[0][colum - 1][2]:
                #         continue
                #     else:
                #         T.insert(END, '\n文件：“' + name + '” 的第“' + str(video_frame_number) + '”帧位深不为8')
                #         break   #不是八位位深则直接检查下个视频
                s = str(video_frame_number).zfill(8)    #添加前导0满足长度为8
                first_line4 = ''    #每帧的第一行前四个字节
                for i in range(4):
                    # value = gray[0][i][0]
                    if frame[0][i][0] < 10:
                        first_line4 = first_line4 + "0" + str(frame[0][i][0])
                    elif frame[0][i][0] == 0:
                        first_line4 = first_line4 + "00"
                    else:
                        first_line4 = first_line4 + str(frame[0][i][0])
                # print first_line4
                if s != first_line4:
                    T.insert(END, '\n文件：“' + name + '” 的第“' + str(video_frame_number) + '”帧的第一行前四个字节为：'+first_line4)
                if height!=600 or width!=800 :
                    T.insert(END, '\n文件：“' + name + '” 的第“'+str(video_frame_number)+'”帧分辨率不为800*600')
            if vn != video_frame_number:
                T.insert(END, '\n文件：“' + name + '”存在帧损，帧数为“' + str(vn) + '”但是只能读取到第：“' + str(video_frame_number) + '”帧。')
            if video_fps!=30 or vn<900 :
                T.insert(END, '\n文件：“' + name + '” 帧率为:'+str(int(video_fps))+',帧数为:'+str(int(vn)))
            change_canvas(file_number, file_all)
    T.insert(END, '\n检查完毕。\n文件夹：' + E1.get() + '，共有' + str(file_number) + '个文件。')
#视频检查按钮组件
b_check_avi=Button(
    F_show5,
    text="视频检查",
    width=20,
    height=2,
    activebackground='lightblue',
    font=12,
    bd=3,
    command = check_avi
)
b_check_avi.pack(side = LEFT)
#------------------------------视频是否有对应标签按钮-------------------------
# 检查每一帧是否有对应的标签组件
def vid_tag_cmp():
    T.insert(END, '开始检查视频每帧否有对应标签.........')
    T.insert(END, '\n注：视频名字（不包含扩展名）要与存放该视频每帧对应标签的文件夹名相同')
    # 判断是否选择文件夹
    if E1.get() == '' or E2.get()== '':
        T.insert(END, '\n抱歉，您未选择视频文件夹或者标签文件夹 \n检查完毕。')
        return
    dir_video_path = E1.get()  # 获取视频文件夹路径
    dir_tag_path = E2.get()  # 获取标签文件夹路径
    file_video_number = 0  # 记录图像文件夹下的文件数量
    # file_tag_number = 0  # 记录标签文件夹下的文件数量
    dictionary = {}
    file_all = 0
    for video_root, video_dirs, videos in os.walk(dir_video_path, topdown=False):
        for video_name in videos:
            file_all += 1
    for video_root, video_dirs, videos in os.walk(dir_video_path, topdown=False):
        for video_name in videos:
            # print '----------------'+video_name+'--------------------------'
            dictionary[video_name] = 0  #用于找同名的标签文件夹
            file_video_number += 1      #记录视频文件夹下视频总数量
            vn = video_name.split('.', 1)[0]  # 截取文件名(文件名-0001)
            #遍历标签文件夹下的文件夹，不遍历子文件，用于找到同视频名的标签文件夹（0001.avi视频就在0001文件夹下找）
            for tag_dir in os.listdir(dir_tag_path):
                #扎到对应文件夹
                if tag_dir==vn:
                    dictionary[video_name] = 1
                    filePath = os.path.join(video_root, video_name)  # 视频绝对路径
                    video_cap = cv2.VideoCapture(filePath)  # 读视频一定成功，之前视频检查按钮读过
                    video_frame_number = video_cap.get(7)  # 帧数
                    #读每一帧
                    for i in range(int(video_frame_number)):
                        # 取得每帧的八位帧号
                        n = i + 1 #（1，2，3，4....）
                        s = str(n).zfill(8)  # 添加前导0满足长度为8(00000001,00000002...)
                        dictionary[s] = 0
                        dirPath = os.path.join(dir_tag_path, tag_dir)  # 获得目标文件夹绝对路径
                        for tag in os.listdir(dirPath):
                            tn = tag.split('.', 1)[0]  # 截取文件名(文件名-00000001)
                            # print (s,tn)
                            if s ==tn:
                                dictionary[s] = 1 #找到对应标签置1,跳出循环
                                break
                        if dictionary[s] == 0:
                            T.insert(END,'\n文件“'+video_name+'”的第“'+str(n)+'”帧没有对应标签')
                # 如果找到了对应文件夹就不用再找
                    break
            if dictionary[video_name] == 0:
                T.insert(END,'\n文件“' + video_name + '”没有对应的标签文件夹')
            change_canvas(file_video_number,file_all)
    T.insert(END, '\n检查完毕。\n文件夹“：' + E1.get() + '”，共有“' + str(file_video_number) + '”个文件。')
# 每帧是否有对应标签按钮组件
b_vid_tag_cmp=Button(
    F_show5,
    text="每帧是否有对应标签",
    width=20,
    height=2,
    activebackground='lightblue',
    font=12,
    bd=3,
    command = vid_tag_cmp
)
b_vid_tag_cmp.pack(side = LEFT)
#------------------------------视频标签检查-------------------
# -- 检查视频标签是否符合七类目标，每个结果都有3个或3个以上的类型，左上坐标，右下坐标，每帧是否提供自定义TAG...
def vid_tag_check():
    T.insert(END, '开始检查视频标签是否符合七类目标，每帧结果都有3个或3个以上的类型，且都有左上坐标，右下坐标，自定义TAG.....')
    # 判断是否选择文件夹
    if E2.get() == '':
        T.insert(END, '\n抱歉，您未选择任何文件夹 \n检查完毕。')
        return
    tag_dir_path = E2.get()  # 获取待检测文件夹路径
    file_number = 0  # 记录文件夹下的文件数量
    file_all = 0
    for tag_root, tag_dirs, tags in os.walk(tag_dir_path, topdown=False):
        for tag_name in tags:
            file_all += 1
    for tag_root, tag_dirs, tags in os.walk(tag_dir_path, topdown=False):
        # 遍历图片文件夹
        for tag_name in tags:
            file_number += 1
            # 打开xml文档
            # print '------------' + tag_name + '---------------------------'
            filePath = os.path.join(tag_root, tag_name)
            dom1 = xml.dom.minidom.parse(filePath)
            # 得到文档元素对象
            root = dom1.documentElement
            # 得到所有name标签,左上坐标，右下坐标,自定义index
            name_list = root.getElementsByTagName('name')
            xmin_list = root.getElementsByTagName('xmin')
            ymin_list = root.getElementsByTagName('ymin')
            xmax_list = root.getElementsByTagName('xmax')
            ymax_list = root.getElementsByTagName('ymax')
            index_list = root.getElementsByTagName('index')
            # 记录个数
            name_len = len(name_list)
            xmin_len = len(xmin_list)
            xmax_len = len(xmax_list)
            ymin_len = len(ymin_list)
            ymax_len = len(ymax_list)
            index_len = len(index_list)
            # 判断都有每个标签
            if name_len == 0 or xmin_len == 0 or xmax_len == 0 or ymin_len == 0 or ymax_len == 0 or index_len==0:
                # print '文件“' + tag_name + '”类型或左上坐标或右下坐标缺失'
                T.insert(END, '\n文件“'+filePath+'”类型或左上坐标或右下坐标或自定义TAG缺失')
                change_canvas(file_number,file_all)
                continue
            # 判断每个标签数量需要相同
            elif name_len != xmin_len or xmin_len != xmax_len or xmax_len != ymin_len or ymin_len != ymax_len or name_len!=index_len:
                # print '文件“' + tag_name + '”类型或左上坐标或右下坐标缺失'
                T.insert(END, '\n文件“'+filePath+'”类型或左上坐标或右下坐标或自定义TAG缺失')
                change_canvas(file_number, file_all)
                continue
            # 判断类型要>=3
            elif name_len<3:
                T.insert(END, '\n文件“'+filePath +'”目标数量小于3')
            # 到达了else说明xml文件都有类型，左上坐标和右下坐标，自定义TAG,且对应，且目标>=3
            else:
                for type_tag in name_list:
                    tn = type_tag.firstChild.data  # 获取标签内数据 tn->type_name
                    if tn != 'plane' and tn != 'runway' and tn != 'airport_oil_depot' and tn != 'vulcans' and tn != 'radar_vehicle' and tn != 'bridge' and tn != 'ship':
                        # print '文件“' + tag_name + '”检测结果类型不符合统一标准'c
                        T.insert(END, '\n文件“'+filePath+'”检测结果类型不符合统一的7类标准')
                        break
            change_canvas(file_number, file_all)
    T.insert(END, '\n检查完毕。\n文件夹：' + E2.get() + '，共有' + str(file_number) + '个文件。')
#视频标签按钮组件
b_check_avi_tag=Button(
    F_show5,
    text="视频标签检查",
    width=20,
    height=2,
    activebackground='lightblue',
    font=12,
    bd=3,
    command = vid_tag_check
)
b_check_avi_tag.pack(side = LEFT)
#----------------------------复位按钮---------------------------
#清空三个文本框
def b_reset():
    # E1.delete(0,END)
    # E2.delete(0, END)
    T.delete("1.0",END)
    text_percent.set('0.00%')
    canvas.delete(ALL)

# 复位按钮组件
b_reset=Button(
    F_show5,
    text="复位",
    width=20,
    height=2,
    activebackground='lightblue',
    font=12,
    bd=3,
    command = b_reset
)
b_reset.pack(side = RIGHT)
#---------------------------------------------------------------

window.mainloop()





