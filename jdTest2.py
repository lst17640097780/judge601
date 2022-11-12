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
if __name__=='__main__':
    #------------------GUI基本信息--------------------------
    window = Tk()
    # 计算机窗口大小  （宽x高）
    window.geometry("800x800")
    window.maxsize(800, 550)
    # 设置计算机title
    window.title("定量指标计算")
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

    #--------------------F_show1，检测结果显示--------------------------
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
    s.config(command = T.yview)#config用来配置tkinter中控件和字体的样式，比如颜色、大小等。
    #---------------------------------------------------------------


    #-----------------------frame_show2，测试结果路径----------------------------
    #单行文本框,测试结果路径Entry（输入框）组件通常用于获取用户的输入文本。如果要替换当前文本，可以先使用 delete() 方法，再使用 insert() 方法实现：
    E1 = Entry(
        F_show2,
        bd =5,
        width=65,
    )
    E1.pack(side = LEFT)
    #-----------------------frame_show2，测试结果路径选择按钮----------------------------
    #选择文件夹函数

    def b_select_DR_xml_dir():    #Detection Result
        E1.delete(0,END)
        default_dir = 'C:\\'  # 默认打开路径
        # 返回文件夹路径

        dirPath = filedialog.askdirectory(title='选择测试结果数据文件夹',
                                          initialdir=r'.\video_tzx')

        # dirPath = tkFileDialog().askdirectory(title='选择标签文件夹', initialdir=default_dir)
        E1.insert(0,dirPath)
    #选择预测结果文件夹按钮
    b_select_dir=Button(
        F_show2,
        text="选择测试结果(test)",
        width=20,
        height=1,
        activebackground='lightblue',
        font=12,
        bd=3,
        command=b_select_DR_xml_dir
    )
    b_select_dir.pack(side = RIGHT)
    #--------------------------------------------------------------------------


    #-----------------------frame_show3，标签数据文件夹路径----------------------------
    #单行文本框,标签数据文件夹
    E2 = Entry(
        F_show3,
        bd =5,
        width=65,
    )
    E2.pack(side = LEFT)
    #-----------------------frame_show3，标签数据文件夹选择按钮----------------------------
    #选择标签文件夹函数
    def b_select_GT_xml_dir():   #GroundTruth
        E2.delete(0,END)
        default_dir = 'C:\\'  # 默认打开路径
        # 返回文件夹路径

        dirPath = filedialog.askdirectory(title='选择标签数据文件夹',
                                          initialdir=r'.\video_tzx')

        E2.insert(0,dirPath)
    #选择标签数据文件夹按钮
    b_select_dir=Button(
        F_show3,
        text="选择标签数据(label)",
        width=20,
        height=1,
        activebackground='lightblue',
        font=12,
        bd=3,
        command=b_select_GT_xml_dir
    )
    b_select_dir.pack(side = RIGHT)


    #--------------------------------查全率检查------------------------------------------
    # --检测出的真实目标个数/所有图像中所有标签个数                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               标表和附录...
    def check_recall():
        T.insert(END, '开始进行查全率检查.........')
        # 判断是否选择文件夹
        if E2.get() == '':
            T.insert(END, '\n抱歉，您未选择标签数据文件夹 \n检查完毕。')
            return
        elif E1.get() == "":
            T.insert(END, '\n抱歉，您未选择预测结果文件夹 \n检查完毕。')
            return
        GT_dir_path = E2.get()  # 获取标签文件夹路径
        DR_dir_path = E1.get()  # 获取检测结果文件夹路径


        class_name = "3"
        def return_fp_number(GT_dir_path,class_name):

            tp_number = 0  # 正确的目标个数
            class_num = 0 #总的目标个数（GT框）
            for tag_root, tag_dirs, tags in os.walk(GT_dir_path, topdown=False):#输入GT文件夹路径，可以直接得到所有正确的预测框数目
                # 遍历图片文件夹
                DR_dir_path = E1.get()  # 获取检测结果文件夹路径
                for tag_name in tags:
                    # 打开xml文档
                    # print '------------' + tag_name + '---------------------------'
                    DTPath = os.path.join(tag_root, tag_name)
                    DRPath = os.path.join(DR_dir_path, tag_name)
                    dom1 = xml.dom.minidom.parse(DTPath)  # 真值
                    dom2 = xml.dom.minidom.parse(DRPath)  # 测试
                    # 得到文档元素对象
                    root = dom1.documentElement
                    root2 = dom2.documentElement
                    # 真实标签
                    name_list = root.getElementsByTagName('index')
                    xmin_list = root.getElementsByTagName('xmin')
                    ymin_list = root.getElementsByTagName('ymin')
                    xmax_list = root.getElementsByTagName('xmax')
                    ymax_list = root.getElementsByTagName('ymax')
                    # 预测标签
                    name_list2 = root2.getElementsByTagName('index')
                    xmin_list2 = root2.getElementsByTagName('xmin')
                    ymin_list2 = root2.getElementsByTagName('ymin')
                    xmax_list2 = root2.getElementsByTagName('xmax')
                    ymax_list2 = root2.getElementsByTagName('ymax')
                    # 获取标签内数据
                    GT_indexs = []  # 真实xml index值
                    DR_indexs = []  # 预测xml index值

                    a = b = c = d = e = f = g = h = -1

                    for type_tag in name_list:
                        index = type_tag.firstChild.data
                        GT_indexs.append(index)  # ['1','2','3']
                    for type_tag2 in name_list2:
                        index2 = type_tag2.firstChild.data
                        DR_indexs.append(index2)
                    GT_axis = [[] for _ in range(len(GT_indexs))]
                    DR_axis = [[] for _ in range(len(DR_indexs))]

                    for xmin in xmin_list:
                        a += 1
                        x1_GT = xmin.firstChild.data
                        GT_axis[a].append(int(x1_GT))
                    for xmin2 in xmin_list2:
                        b += 1
                        x1_DR = xmin2.firstChild.data
                        DR_axis[b].append(int(x1_DR))
                    for ymin in ymin_list:
                        c += 1
                        y1_GT = ymin.firstChild.data
                        GT_axis[c].append(int(y1_GT))
                    for ymin2 in ymin_list2:
                        d += 1
                        y1_DR = ymin2.firstChild.data
                        DR_axis[d].append(int(y1_DR))
                    for xmax in xmax_list:
                        e += 1
                        x2_GT = xmax.firstChild.data
                        GT_axis[e].append(int(x2_GT))
                    for xmax2 in xmax_list2:
                        f += 1
                        x2_DR = xmax2.firstChild.data
                        DR_axis[f].append(int(x2_DR))
                    for ymax in ymax_list:
                        g += 1
                        y2_GT = ymax.firstChild.data
                        GT_axis[g].append(int(y2_GT))
                    for ymax2 in ymax_list2:
                        h += 1
                        y2_DR = ymax2.firstChild.data
                        DR_axis[h].append(int(y2_DR))
                    # 判断是否预测正确

                    j = -1
                    # tr = []
                    for GT_index in GT_indexs:
                        j += 1
                        if GT_index == class_name:
                            class_num += 1
                            if GT_index in DR_indexs:#只要当前的GT框在DR列表中，就进行比对
                                cou = DR_indexs.count(GT_index)  # 标号的个数
                                tmp = -1
                                IOUS = []  # 重复框的IOU
                                tr_tmp = []  # 不去掉重复框的预测正确的idex
                                for k in range(cou):
                                    tmp = DR_indexs.index(GT_index, tmp + 1, len(DR_indexs))
                                    IOU = calculateIou(GT_axis[j], DR_axis[tmp])
                                    if IOU >= 0.5:
                                        IOUS.append(IOU)
                                        tr_tmp.append(GT_indexs[j])
                                if len(IOUS) > 1:
                                    max_iou = max(IOUS)
                                    max_iou_index = IOUS.index(max_iou)
                                    tp_number += 1
                                elif len(IOUS) == 1:
                                    tp_number += 1

                                # tr.append(GT_indexs[j])
            return tp_number,class_num

        a,b = return_fp_number(GT_dir_path,class_name)
        print(a,b)
        # DR_object_number = ...
        # GT_object_number = ...
        # recall_result = DR_object_number/GT_object_number
        # T.insert(END, '\n检查完毕。\图片检测的查全率为：'+ recall_result )
    # 查全率检查按钮组件
    b_check_img=Button(
        F_show4,
        text="查全率检查",
        width=20,
        height=2,
        activebackground='lightblue',
        font=12,
        bd=3,
        command=check_recall,
    )
    b_check_img.pack(side = LEFT)
    #------------------------------图像是否有对应标签按钮-------------------------
    # --详见目标表和附录...
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
    # 查准率检查组件按钮
    b_img_tag_cmp=Button(
        F_show4,
        text="查准率检查",
        width=20,
        height=2,
        activebackground='lightblue',
        font=12,
        bd=3,
        command = img_tag_cmp
    )
    b_img_tag_cmp.pack(side = LEFT)
    #--------------------------------识别率检查----------------------------------
    # --详见目标表和附录...
    def calculateIou(box1, box2):
        x1, y1, x2, y2 = box1
        xx1, yy1, xx2, yy2 = box2

        # 交
        w = max(0, min(x2, xx2) - max(x1, xx1))
        h = max(0, min(y2, yy2) - max(y1, yy1))
        interarea = w * h

        # 并
        union = (x2 - x1) * (y2 - y1) + (xx2 - xx1) * (yy2 - yy1) - interarea

        # 交并比
        return interarea / union
    def check_recognize():
        T.insert(END, '\n开始进行识别率检测.........')
        # 判断是否选择文件夹
        if E2.get() == '':
            T.insert(END, '\n抱歉，您未选择标签数据文件夹 \n检查完毕。')
            return
        elif E1.get() == "":
            T.insert(END, '\n抱歉，您未选择预测结果文件夹 \n检查完毕。')
            return
        GT_dir_path = E2.get()  # 获取标签文件夹路径
        DR_dir_path = E1.get()  # 获取检测结果文件夹路径
        true_obj = 0  # 正确的目标个数
        true_all = 0  # 图片上所有目标都识别正确的概率
        true_DRpics = {}  # 预测正确的图像和对应的标签
        GT_pics={}#标注的图片和对应标签
        for tag_root, tag_dirs, tags in os.walk(GT_dir_path, topdown=False):
            # 遍历图片文件夹
            for tag_name in tags:
                # 打开xml文档
                # print '------------' + tag_name + '---------------------------'
                DTPath = os.path.join(tag_root, tag_name)
                DRPath = os.path.join(DR_dir_path, tag_name)
                dom1 = xml.dom.minidom.parse(DTPath)  # 真值
                dom2 = xml.dom.minidom.parse(DRPath)  # 测试
                # 得到文档元素对象
                root = dom1.documentElement
                root2 = dom2.documentElement
                # 真实标签
                name_list = root.getElementsByTagName('index')
                xmin_list = root.getElementsByTagName('xmin')
                ymin_list = root.getElementsByTagName('ymin')
                xmax_list = root.getElementsByTagName('xmax')
                ymax_list = root.getElementsByTagName('ymax')
                # 预测标签
                name_list2 = root2.getElementsByTagName('index')
                xmin_list2 = root2.getElementsByTagName('xmin')
                ymin_list2 = root2.getElementsByTagName('ymin')
                xmax_list2 = root2.getElementsByTagName('xmax')
                ymax_list2 = root2.getElementsByTagName('ymax')
                # 获取标签内数据
                GT_indexs = []  # 真实xml index值
                DR_indexs = []  # 预测xml index值

                a = b = c = d = e = f = g = h = -1

                for type_tag in name_list:
                    index = type_tag.firstChild.data
                    GT_indexs.append(index)  # ['1','2','3']
                for type_tag2 in name_list2:
                    index2 = type_tag2.firstChild.data
                    DR_indexs.append(index2)
                GT_axis = [[] for _ in range(len(GT_indexs))]
                DR_axis = [[] for _ in range(len(DR_indexs))]

                for xmin in xmin_list:
                    a += 1
                    x1_GT = xmin.firstChild.data
                    GT_axis[a].append(int(x1_GT))
                for xmin2 in xmin_list2:
                    b += 1
                    x1_DR = xmin2.firstChild.data
                    DR_axis[b].append(int(x1_DR))
                for ymin in ymin_list:
                    c += 1
                    y1_GT = ymin.firstChild.data
                    GT_axis[c].append(int(y1_GT))
                for ymin2 in ymin_list2:
                    d += 1
                    y1_DR = ymin2.firstChild.data
                    DR_axis[d].append(int(y1_DR))
                for xmax in xmax_list:
                    e += 1
                    x2_GT = xmax.firstChild.data
                    GT_axis[e].append(int(x2_GT))
                for xmax2 in xmax_list2:
                    f += 1
                    x2_DR = xmax2.firstChild.data
                    DR_axis[f].append(int(x2_DR))
                for ymax in ymax_list:
                    g += 1
                    y2_GT = ymax.firstChild.data
                    GT_axis[g].append(int(y2_GT))
                for ymax2 in ymax_list2:
                    h += 1
                    y2_DR = ymax2.firstChild.data
                    DR_axis[h].append(int(y2_DR))
                # 判断是否预测正确

                j = -1
                tr = []
                for GT_index in GT_indexs:
                    j += 1
                    if GT_index in DR_indexs:
                        i = DR_indexs.index(GT_index)
                        IOU = calculateIou(GT_axis[j], DR_axis[i])
                        if IOU >= 0.5:
                            true_obj += 1
                            tr.append(GT_indexs[j])
                true_DRpics[tag_name] = tr
                GT_pics[tag_name]=GT_indexs
                if len(GT_indexs) == len(DR_indexs) == len(tr):
                    true_all += 1  #
        # 识别率
        acc_recongnize = round((true_all / len(tags)), 5)
        # 虚警率
        acc_warm = 1 - acc_recongnize
        T.insert(END, '\n检查完毕。\图片检测的识别率为：' + str(acc_recongnize*100)+"%")
        return(true_obj,true_DRpics,GT_pics)

    # 识别率检查按钮组件
    b_check_img_tag=Button(
        F_show4,
        text="识别率检查",
        width=20,
        height=2,
        activebackground='lightblue',
        font=12,
        bd=3,
        command = check_recognize
    )
    b_check_img_tag.pack(side = LEFT)
    #-----------------------------虚警率检查---------------------
    def check_warm_tar():
        T.insert(END, '\n开始进行虚警率检测.........')
        # 判断是否选择文件夹
        if E2.get() == '':
            T.insert(END, '\n抱歉，您未选择标签数据文件夹 \n检查完毕。')
            return
        elif E1.get() == "":
            T.insert(END, '\n抱歉，您未选择预测结果文件夹 \n检查完毕。')
            return
        GT_dir_path = E2.get()  # 获取标签文件夹路径
        DR_dir_path = E1.get()  # 获取检测结果文件夹路径
        true_obj = 0  # 正确的目标个数
        true_all = 0  # 图片上所有目标都识别正确的概率
        true_DRpics = {}  # 预测正确的图像和对应的标签
        GT_pics = {}  # 标注的图片和对应标签
        for tag_root, tag_dirs, tags in os.walk(GT_dir_path, topdown=False):
            # 遍历图片文件夹
            for tag_name in tags:
                # 打开xml文档
                # print '------------' + tag_name + '---------------------------'
                DTPath = os.path.join(tag_root, tag_name)
                DRPath = os.path.join(DR_dir_path, tag_name)
                dom1 = xml.dom.minidom.parse(DTPath)  # 真值
                dom2 = xml.dom.minidom.parse(DRPath)  # 测试
                # 得到文档元素对象
                root = dom1.documentElement
                root2 = dom2.documentElement
                # 真实标签
                name_list = root.getElementsByTagName('index')
                xmin_list = root.getElementsByTagName('xmin')
                ymin_list = root.getElementsByTagName('ymin')
                xmax_list = root.getElementsByTagName('xmax')
                ymax_list = root.getElementsByTagName('ymax')
                # 预测标签
                name_list2 = root2.getElementsByTagName('index')
                xmin_list2 = root2.getElementsByTagName('xmin')
                ymin_list2 = root2.getElementsByTagName('ymin')
                xmax_list2 = root2.getElementsByTagName('xmax')
                ymax_list2 = root2.getElementsByTagName('ymax')
                # 获取标签内数据
                GT_indexs = []  # 真实xml index值
                DR_indexs = []  # 预测xml index值

                a = b = c = d = e = f = g = h = -1

                for type_tag in name_list:
                    index = type_tag.firstChild.data
                    GT_indexs.append(index)  # ['1','2','3']
                for type_tag2 in name_list2:
                    index2 = type_tag2.firstChild.data
                    DR_indexs.append(index2)
                GT_axis = [[] for _ in range(len(GT_indexs))]
                DR_axis = [[] for _ in range(len(DR_indexs))]

                for xmin in xmin_list:
                    a += 1
                    x1_GT = xmin.firstChild.data
                    GT_axis[a].append(int(x1_GT))
                for xmin2 in xmin_list2:
                    b += 1
                    x1_DR = xmin2.firstChild.data
                    DR_axis[b].append(int(x1_DR))
                for ymin in ymin_list:
                    c += 1
                    y1_GT = ymin.firstChild.data
                    GT_axis[c].append(int(y1_GT))
                for ymin2 in ymin_list2:
                    d += 1
                    y1_DR = ymin2.firstChild.data
                    DR_axis[d].append(int(y1_DR))
                for xmax in xmax_list:
                    e += 1
                    x2_GT = xmax.firstChild.data
                    GT_axis[e].append(int(x2_GT))
                for xmax2 in xmax_list2:
                    f += 1
                    x2_DR = xmax2.firstChild.data
                    DR_axis[f].append(int(x2_DR))
                for ymax in ymax_list:
                    g += 1
                    y2_GT = ymax.firstChild.data
                    GT_axis[g].append(int(y2_GT))
                for ymax2 in ymax_list2:
                    h += 1
                    y2_DR = ymax2.firstChild.data
                    DR_axis[h].append(int(y2_DR))
                # 判断是否预测正确

                j = -1
                tr = []
                for GT_index in GT_indexs:
                    j += 1
                    if GT_index in DR_indexs:
                        i = DR_indexs.index(GT_index)
                        IOU = calculateIou(GT_axis[j], DR_axis[i])
                        if IOU >= 0.5:
                            true_obj += 1
                            tr.append(GT_indexs[j])
                true_DRpics[tag_name] = tr
                GT_pics[tag_name] = GT_indexs
                if len(GT_indexs) == len(DR_indexs) == len(tr):
                    true_all += 1  #
        # 识别率
        acc_recongnize = round((true_all / len(tags)), 5)
        # 虚警率
        acc_warm = 1 - acc_recongnize
        T.insert(END, '\n检查完毕。\图片检测的虚警率为：' + str(acc_warm*100)+"%")


    # 虚警率检查按钮组件
    b_check_img_tag=Button(
        F_show4,
        text="虚警率检查",
        width=20,
        height=2,
        activebackground='lightblue',
        font=12,
        bd=3,
        command = check_warm_tar
    )
    b_check_img_tag.pack(side = LEFT)
    #-----------------------frame_show5，视频类按钮+复位---------------------------
    #-----------------------------识别速度检查------------------------
    # --详见目标表和附录...
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
    #识别速度检查按钮组件
    b_check_avi=Button(
        F_show5,
        text="识别速度检查",
        width=20,
        height=2,
        activebackground='lightblue',
        font=12,
        bd=3,
        command = check_avi
    )
    b_check_avi.pack(side = LEFT)
    #------------------------------目标编号一致性检查-------------------------
    # 详见目标表和附录
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
    # 目标编号一致性检查按钮组件
    b_vid_tag_cmp=Button(
        F_show5,
        text="目标编号一致性检查",
        width=20,
        height=2,
        activebackground='lightblue',
        font=12,
        bd=3,
        command = vid_tag_cmp
    )
    b_vid_tag_cmp.pack(side = LEFT)
    #------------------------------导出日志-------------------
    # -- 生成日志文件并导出...
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
    #导出日志按钮组件
    b_check_avi_tag=Button(
        F_show5,
        text="导出日志",
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





