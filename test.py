

#=================================load—image====================
# import cv2
# # img_path = r"C:\Users\Administrator\Desktop\601目标检测\PyProject1\video_tzx\BMP\0001.bmp"#这里是我的单通道灰度图
# img_path = "./video_tzx/BMP/0001.bmp"#这里是我的单通道灰度图
# # img = cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
# img = cv2.imread(r'D:\PycharmProjects\PyProject1\video_tzx\BMP\0001.bmp',cv2.IMREAD_GRAYSCALE)
# cv2.imshow("1",img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



#===============================IOU-test========================
#
#
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
        print(iou)

rec_1=(673, 38, 683, 48)                     #四个值分别为左上角顶点（x1,y1），右下角坐标（x2,y2）

rec_2=(663, 28, 683, 48)
compute_iou(rec_1,rec_2)


#===============================load_xml-test========================
# import os
# import xml.dom.minidom
#
# for tag_root, tag_dirs, tags in os.walk('D:/PycharmProjects/PyProject1/video_tzx/xml_label_1_250', topdown=False):
#     # 遍历图片文件夹
#     DR_rec_list = []
#     file_number = 0  # 记录文件夹下的文件数量
#     small_plane = 0  # 记录飞机类小目标图像数
#     GT_object_number = 0
#
#     for tag_name in tags:
#         file_number += 1
#         # 打开xml文档
#         # print '------------' + tag_name + '---------------------------'
#         filePath = os.path.join(tag_root, tag_name)
#         dom = xml.dom.minidom.parse(filePath)
#         # 得到文档元素对象
#         root = dom.documentElement
#         # 得到所有name标签,左上坐标，右下坐标
#         name_list = root.getElementsByTagName('category')
#         xmin_list = root.getElementsByTagName('xmin')
#         ymin_list = root.getElementsByTagName('ymin')
#         xmax_list = root.getElementsByTagName('xmax')
#         ymax_list = root.getElementsByTagName('ymax')
#         for i, type_name in enumerate(name_list):
#             GT_object_number += 1
#             DR_rec_list.append((int(xmin_list[i].firstChild.data),int(ymin_list[i].firstChild.data),int(xmax_list[i].firstChild.data),int(ymax_list[i].firstChild.data)))
#             print(DR_rec_list)
#             a = input()
#             # print(i)
#             # print(file_number)

#===========================================================================

import numpy as np

#
# for d in range(nd):
#     R = class_recs[image_ids[d]]
#     bb = BB[d, :].astype(float)
#     ovmax = -np.inf
#     # BBGT = R['bbox'].astype(float)  # ground truth
#
#     if BBGT.size > 0:
#         # 计算IoU
#         # intersection
#         ixmin = np.maximum(BBGT[:, 0], bb[0])
#         iymin = np.maximum(BBGT[:, 1], bb[1])
#         ixmax = np.minimum(BBGT[:, 2], bb[2])
#         iymax = np.minimum(BBGT[:, 3], bb[3])
#         iw = np.maximum(ixmax - ixmin + 1., 0.)
#         ih = np.maximum(iymax - iymin + 1., 0.)
#         inters = iw * ih
#
#         # union
#         uni = ((bb[2] - bb[0] + 1.) * (bb[3] - bb[1] + 1.) +
#                (BBGT[:, 2] - BBGT[:, 0] + 1.) *
#                (BBGT[:, 3] - BBGT[:, 1] + 1.) - inters)
#
#         overlaps = inters / uni
#         ovmax = np.max(overlaps)
#         jmax = np.argmax(overlaps)
#     # 取最大的IoU
#     if ovmax > 0.5:  # 是否大于阈值
#         if not R['difficult'][jmax]:  # 非difficult物体
#             if not R['det'][jmax]:  # 未被检测
#                 tp[d] = 1.
#                 R['det'][jmax] = 1  # 标记已被检测
#             else:
#                 fp[d] = 1.
#     else:
#         fp[d] = 1.
#
# # 计算precision recall
# fp = np.cumsum(fp)
# tp = np.cumsum(tp)
# rec = tp / float(npos)
#
#
# BBGT = np.array([673, 38, 683, 48])
#
# bb = np.array([683, 28, 683, 48])
# if BBGT.size > 0:
# # 计算IoU
# # intersection
#     ixmin = np.maximum(BBGT[0], bb[0])
#     iymin = np.maximum(BBGT[1], bb[1])
#     ixmax = np.minimum(BBGT[2], bb[2])
#     iymax = np.minimum(BBGT[3], bb[3])
#     iw = np.maximum(ixmax - ixmin + 1., 0.)
#     ih = np.maximum(iymax - iymin + 1., 0.)
#     inters = iw * ih
#
#     # union
#     uni = ((bb[2] - bb[0] + 1.) * (bb[3] - bb[1] + 1.) +
#            (BBGT[2] - BBGT[0] + 1.) *
#            (BBGT[3] - BBGT[1] + 1.) - inters)
#
#     overlaps = inters / uni
#     ovmax = np.max(overlaps)
#     jmax = np.argmax(overlaps)
# print(overlaps)
# print(inters)