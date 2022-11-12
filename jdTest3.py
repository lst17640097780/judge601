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
s.config(command = T.yview)
#---------------------------------------------------------------


#-----------------------frame_show2，测试结果路径----------------------------
#单行文本框,测试结果路径
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
#==IOU计算
def compute_iou(rec_1,rec_2):
    '''
    rec_1:左上角(rec_1[0],rec_1[1])    右下角：(rec_1[2],rec_1[3])
    rec_2:左上角(rec_2[0],rec_2[1])    右下角：(rec_2[2],rec_2[3])

    （rec_1）
    1--------1
    1   1----1------1
    1---1----1      1
        1           1
        1-----------1 （rec_2）
    '''
    s_rec1=(rec_1[2]-rec_1[0])*(rec_1[3]-rec_1[1])   #第一个bbox面积 = 长×宽
    s_rec2=(rec_2[2]-rec_2[0])*(rec_2[3]-rec_2[1])   #第二个bbox面积 = 长×宽
    sum_s=s_rec1+s_rec2                              #总面积
    left=max(rec_1[0],rec_2[0])                      #并集左上角顶点横坐标
    right=min(rec_1[2],rec_2[2])                     #并集右下角顶点横坐标
    bottom=max(rec_1[1],rec_2[1])                    #并集左上角顶点纵坐标
    top=min(rec_1[3],rec_2[3])                       #并集右下角顶点纵坐标
    if left >= right or top <= bottom:               #不存在并集的情况
        return 0
    else:
        inter=(right-left)*(top-bottom)              #求并集面积
        iou=(inter/(sum_s-inter))*1.0                #计算IOU
        return(iou)
#==统计各种数目
def tp_fp_num(GT_dir_path, DR_dir_path,class_name, class_number, tp_number, fp_number, file_number,file_all):
    """
    :param GT_dir_path: 标注框的路径
    :param class_name: 类名称，如：“plane”
    :param class_number: 需要计算的类目总数
    :param tp_number: 正确预测的数目
    :param fp_number: 错误预测的数目
    :param file_number: 已经检测的文件数目，用于进度条
    :param file_all: 进度条数据
    :return: class_number, fp_number, tp_number, file_number
    """
    for tag_root, tag_dirs, tags in os.walk(GT_dir_path, topdown=False):
        # 遍历图片文件夹
        for tag_name in tags:
            file_number += 1
            # 打开xml文档
            # print '------------' + tag_name + '---------------------------'
            filePath = os.path.join(tag_root, tag_name)
            dom = xml.dom.minidom.parse(filePath)
            # 得到文档元素对象
            root = dom.documentElement
            # 得到所有name标签
            name_list = root.getElementsByTagName('category')
            xmin_list = root.getElementsByTagName('xmin')
            ymin_list = root.getElementsByTagName('ymin')
            xmax_list = root.getElementsByTagName('xmax')
            ymax_list = root.getElementsByTagName('ymax')

            # 以下为读取同名文件中的预测框信息，并汇集为DR数据表格
            DR_rec_list = []  # 在这里创建DR矩阵，可以有效保留flag信息
            dete_tag_root = DR_dir_path  # 检测标签目录的路径
            dete_filePath = os.path.join(dete_tag_root, tag_name)  # 检测标签目录的路径下的同名文件夹
            dete_dom = xml.dom.minidom.parse(dete_filePath)  # 得到文档元素对象
            dete_root = dete_dom.documentElement  # 得到所有name标签
            dete_name_list = dete_root.getElementsByTagName('category')
            dete_xmin_list = dete_root.getElementsByTagName('xmin')
            dete_ymin_list = dete_root.getElementsByTagName('ymin')
            dete_xmax_list = dete_root.getElementsByTagName('xmax')
            dete_ymax_list = dete_root.getElementsByTagName('ymax')
            dete_confidence_list = dete_root.getElementsByTagName('confidence')
            for i, type_name in enumerate(dete_name_list):
                dete_tn = type_name.firstChild.data  # 记录name标签内的数据
                catagory = dete_tn
                x1 = float(dete_xmin_list[i].firstChild.data)
                y1 = float(dete_ymin_list[i].firstChild.data)
                x2 = float(dete_xmax_list[i].firstChild.data)
                y2 = float(dete_ymax_list[i].firstChild.data)
                confidence = float(dete_confidence_list[i].firstChild.data)
                flag = 0  # flag=0待测，flag = 1为tp，flag = -1为fp
                # 压缩进DR数据表格的第一行，依次类推
                DR_rec_list.append([catagory, x1, y1, x2, y2, confidence, flag])
            # 先按照置信度排列表格
            DR_rec_list.sort(key=lambda tup: tup[5], reverse=True)

            # 从当前的GT文件中寻找飞机目标
            for i, type_name in enumerate(name_list):
                tn = type_name.firstChild.data  # 记录name标签内的数据

                if tn == class_name:
                    GT_rec = ((float(xmin_list[i].firstChild.data), float(ymin_list[i].firstChild.data),
                               float(xmax_list[i].firstChild.data), float(ymax_list[i].firstChild.data)))

                    # 如果找到了一个飞机目标，还需要急需往下遍历，不能跳出循环（为了防止一个图片中两个飞机）（以前是直接跳出去了）
                    class_number += 1

                    # 从DR数据表格中依次取值进行iou计算，并刷新表格
                    for i in range(len(DR_rec_list)):
                        DR_rec = (DR_rec_list[i][1], DR_rec_list[i][2], DR_rec_list[i][3], DR_rec_list[i][4])
                        if DR_rec_list[i][0] == class_name and DR_rec_list[i][6] == 0:  # 先筛选出同名的类
                            iou = compute_iou(GT_rec, DR_rec)
                            if iou > 0.5:  # Iou大于0.5，则有对的可能
                                DR_rec_list[i][6] = iou
                            else:
                                DR_rec_list[i][6] = -1

                    # 在当前的GT框下，进行最优的预测框选取
                    iou_max = max(DR_rec_list, key=lambda x: x[6])[6]
                    for i in range(len(DR_rec_list)):
                        if DR_rec_list[i][6] != 0:#不等于0，也就是说不是其他类
                            if DR_rec_list[i][6] == -1:
                                fp_number += 1
                                DR_rec_list[i][6] = 0 #置为0，也就是下一波还测它
                            elif DR_rec_list[i][6] == iou_max:  # 取最大的flag那行，tp+1，否则，flag置为0
                                tp_number += 1
                            else:
                                DR_rec_list[i][6] = 0#那些虽然IOU也大于0.5，但是不够最大的，下一波还测它

            change_canvas(file_number, file_all)
    return class_number,  tp_number, fp_number, file_number


def check_P_R():

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

    file_number = 0  # 记录文件夹下的文件数量
    file_all = 0
    # --七类目标总数--
    plane_number = 0
    runway_number = 0
    airportOilDepot_number = 0
    vulcans_number = 0
    radarVehicle_number = 0
    bridge_number = 0
    ship_number = 0

    # --七类目标的检测正确总数--
    plane_tp_number = 0
    runway_tp_number = 0
    airportOilDepot_tp_number = 0
    vulcans_tp_number = 0
    radarVehicle_tp_number = 0
    bridge_tp_number = 0
    ship_tp_number = 0

    # --七类目标的检测错误总数--
    plane_fp_number = 0
    runway_fp_number = 0
    airportOilDepot_fp_number = 0
    vulcans_fp_number = 0
    radarVehicle_fp_number = 0
    bridge_fp_number = 0
    ship_fp_number = 0

    # 先记录文件总数用于进度条
    for tag_root, tag_dirs, tags in os.walk(GT_dir_path, topdown=False):
        for tag_name in tags:
            file_all += 1
    file_all *= 7
    # --------------------计算飞机类图像数--------------
    plane_number, plane_tp_number, plane_fp_number, file_number = tp_fp_num(GT_dir_path,DR_dir_path, "1", plane_number, plane_tp_number, plane_fp_number, file_number,file_all)
    # --------------------计算机场跑道类图像数--------------
    runway_number, runway_tp_number, runway_fp_number, file_number = tp_fp_num(GT_dir_path, DR_dir_path, "2", runway_number,
                                                                            runway_tp_number, runway_fp_number,
                                                                            file_number,file_all)
    # --------------------计算机场油库类图像数--------------
    airportOilDepot_number, airportOilDepot_tp_number, airportOilDepot_fp_number, file_number = tp_fp_num(GT_dir_path, DR_dir_path, "3", airportOilDepot_number,
                                                                            airportOilDepot_tp_number, airportOilDepot_fp_number,
                                                                            file_number,file_all)
    # --------------------计算地空导弹车类图像数--------------
    vulcans_number, vulcans_tp_number, vulcans_fp_number, file_number = tp_fp_num(GT_dir_path,DR_dir_path, "4", vulcans_number, vulcans_tp_number, vulcans_fp_number, file_number,file_all)
    # --------------------计算地/海面防空雷达车类图像数--------------
    radarVehicle_number, radarVehicle_tp_number, radarVehicle_fp_number, file_number = tp_fp_num(GT_dir_path,DR_dir_path, "5", radarVehicle_number, radarVehicle_tp_number, radarVehicle_fp_number, file_number,file_all)
    # --------------------计算桥梁类图像数--------------
    bridge_number, bridge_tp_number, bridge_fp_number, file_number = tp_fp_num(GT_dir_path, DR_dir_path, "6", bridge_number,
                                                                            bridge_tp_number, bridge_fp_number,
                                                                            file_number,file_all)
    # --------------------计算运输舰艇类图像数--------------
    ship_number, ship_tp_number, ship_fp_number, file_number = tp_fp_num(GT_dir_path, DR_dir_path, "7", ship_number,
                                                                            ship_tp_number, ship_fp_number,
                                                                            file_number,file_all)
    #-----------------------计算完毕，显示结果-------------
    plane_recall = plane_tp_number/plane_number
    plane_precision = plane_tp_number/(plane_tp_number+plane_fp_number)
    runway_recall = runway_tp_number / runway_number
    runway_precision = runway_tp_number / (runway_tp_number + runway_fp_number)
    airportOilDepot_recall = airportOilDepot_tp_number / airportOilDepot_number
    airportOilDepot_precision = airportOilDepot_tp_number / (airportOilDepot_tp_number + airportOilDepot_fp_number)
    vulcans_recall = vulcans_tp_number / vulcans_number
    vulcans_precision = vulcans_tp_number / (vulcans_tp_number + vulcans_fp_number)
    # radarVehicle_recall = radarVehicle_tp_number / radarVehicle_number
    # radarVehicle_precision = radarVehicle_tp_number / (radarVehicle_tp_number + radarVehicle_fp_number)
    # bridge_recall = bridge_tp_number / bridge_number
    # bridge_precision = bridge_tp_number / (bridge_tp_number + bridge_fp_number)
    # ship_recall = ship_tp_number / ship_number
    # ship_precision = ship_tp_number / (ship_tp_number + ship_fp_number)
    # 七类目标图像数
    T.insert(END, '\n\n统计七类目标的数目如下：')
    T.insert(END, '\n"飞机"类目标共有“' + str(plane_number) + '”个，'+'其中被正确检测的目标共有“'+str(plane_tp_number) + '”个，'+'被错误检测的目标共有”'+str(plane_fp_number) + '”个')
    T.insert(END, '\n"该类检测的查全率为“' + str(plane_recall)+'”,查准率为“'+str(plane_precision)+'“')

    T.insert(END, '\n"机场跑道"类目标共有“' + str(runway_number) + '”个，' + '其中被正确检测的目标共有“' + str(
        runway_tp_number) + '”个，' + '被错误检测的目标共有”' + str(runway_fp_number) + '”个')
    T.insert(END, '\n"该类检测的查全率为“' + str(runway_recall) + '”,查准率为“' + str(runway_precision) + '“')

    T.insert(END, '\n"机场油库"类目标共有“' + str(airportOilDepot_number) + '”个，' + '其中被正确检测的目标共有“' + str(
        airportOilDepot_tp_number) + '”个，' + '被错误检测的目标共有”' + str(airportOilDepot_fp_number) + '”个')
    T.insert(END, '\n"该类检测的查全率为“' + str(airportOilDepot_recall) + '”,查准率为“' + str(airportOilDepot_precision) + '“')

    T.insert(END, '\n"地空导弹车"类目标共有“' + str(vulcans_number) + '”个，' + '其中被正确检测的目标共有“' + str(
        vulcans_tp_number) + '”个，' + '被错误检测的目标共有”' + str(vulcans_fp_number) + '”个')
    T.insert(END, '\n"该类检测的查全率为“' + str(vulcans_recall) + '”,查准率为“' + str(vulcans_precision) + '“')
    # T.insert(END, '\n"地/海面防空雷达车"类目标共有“' + str(radarVehicle_number) + '”个，' + '其中被正确检测的目标共有“' + str(
    #     radarVehicle_tp_number) + '”个，' + '被错误检测的目标共有”' + str(radarVehicle_fp_number) + '”个')
    # T.insert(END, '\n"该类检测的查全率为“' + str(radarVehicle_recall) + '”,查准率为“' + str(radarVehicle_precision) + '“')
    # T.insert(END, '\n"桥梁"类目标共有“' + str(bridge_number) + '”个，' + '其中被正确检测的目标共有“' + str(
    #     bridge_tp_number) + '”个，' + '被错误检测的目标共有”' + str(bridge_fp_number) + '”个')
    # T.insert(END, '\n"该类检测的查全率为“' + str(bridge_recall) + '”,查准率为“' + str(bridge_precision) + '“')
    # T.insert(END, '\n"运输舰艇"类目标共有“' + str(ship_number) + '”个，' + '其中被正确检测的目标共有“' + str(
    #     ship_tp_number) + '”个，' + '被错误检测的目标共有”' + str(ship_fp_number) + '”个')
    # T.insert(END, '\n"该类检测的查全率为“' + str(ship_recall) + '”,查准率为“' + str(ship_precision) + '“')

    T.insert(END, '\n\n检查完毕。')
    T.insert(END, '\n文件夹下共有“' + str(file_number / 7) + '”个文件')


# 查全率检查按钮组件
b_check_img=Button(
    F_show4,
    text="查全率和查准率检查",
    width=40,
    height=2,
    activebackground='lightblue',
    font=12,
    bd=3,
    command=check_P_R,
)
b_check_img.pack(side = LEFT)

#--------------------------------识别率检查----------------------------------

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
    true_all = 0  # 图片上所有目标都识别正确的概率
    true_DRpics = {}  # 预测正确的图像和对应的标签
    GT_pics = {}  # 标注的图片和对应标签

    file_all = 0
    file_number = 0
    for tag_root, tag_dirs, tags in os.walk(GT_dir_path, topdown=False):
        for tag_name in tags:
            file_all += 1
    file_all *= 1

    for tag_root, tag_dirs, tags in os.walk(GT_dir_path, topdown=False):
        # 遍历图片文件夹
        for tag_name in tags:
            file_number += 1
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
            tr = []  # 去除重复框后的正确预测的标签值
            for GT_index in GT_indexs:
                j += 1
                if GT_index in DR_indexs:
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
                            # tr.append(GT_indexs[j])
                    if len(IOUS) > 1:
                        max_iou = max(IOUS)
                        max_iou_index = IOUS.index(max_iou)
                        tr.append(tr_tmp[max_iou_index])
                    elif len(IOUS) == 1:
                        tr.append(tr_tmp[0])
            true_DRpics[tag_name] = tr
            GT_pics[tag_name] = GT_indexs
            if len(GT_indexs) == len(tr):
                true_all += 1
            change_canvas(file_number, file_all)
    # 识别率
    acc_recongnize = round((true_all / len(tags)), 5)
    # 虚警率
    acc_warm = 1 - acc_recongnize
    T.insert(END, '\n检查完毕。\图片检测的识别率为：' + str(acc_recongnize * 100) + "%")
    return (true_DRpics, GT_pics)
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
# --详见目标表和附录...
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
    true_all = 0  # 图片上所有目标都识别正确的概率
    true_DRpics = {}  # 预测正确的图像和对应的标签
    GT_pics = {}  # 标注的图片和对应标签

    file_all = 0
    file_number = 0
    for tag_root, tag_dirs, tags in os.walk(GT_dir_path, topdown=False):
        for tag_name in tags:
            file_all += 1
    file_all *= 1

    for tag_root, tag_dirs, tags in os.walk(GT_dir_path, topdown=False):

        # 遍历图片文件夹
        for tag_name in tags:
            file_number += 1
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
            tr = []  # 去除重复框后的正确预测的标签值
            for GT_index in GT_indexs:
                j += 1
                if GT_index in DR_indexs:
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
                            # tr.append(GT_indexs[j])
                    if len(IOUS) > 1:
                        max_iou = max(IOUS)
                        max_iou_index = IOUS.index(max_iou)
                        tr.append(tr_tmp[max_iou_index])
                    elif len(IOUS) == 1:
                        tr.append(tr_tmp[0])
            true_DRpics[tag_name] = tr
            GT_pics[tag_name] = GT_indexs
            if len(GT_indexs) == len(tr):
                true_all += 1

            change_canvas(file_number, file_all)
    # 识别率
    acc_recongnize = round((true_all / len(tags)), 5)
    # 虚警率
    acc_warm = 1 - acc_recongnize
    T.insert(END, '\n检查完毕。\图片检测的虚警率为：' + str(acc_warm * 100) + "%")
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





