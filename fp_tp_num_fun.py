
    for tag_root, tag_dirs, tags in os.walk(GT_dir_path, topdown=False):
        for tag_name in tags:
            file_all += 1
    file_all *= 7
    # --------------------计算飞机类图像数--------------
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
                flag = 0  #flag=0待测，flag = 1为tp，flag = -1为fp
                # 压缩进DR数据表格的第一行，依次类推
                DR_rec_list.append([catagory, x1, y1, x2, y2, confidence, flag])
            # 先按照置信度排列表格
            DR_rec_list.sort(key=lambda tup: tup[5],reverse=True)


            # 从当前的GT文件中寻找飞机目标
            for i,type_name in enumerate(name_list):
                tn = type_name.firstChild.data  # 记录name标签内的数据

                if tn == '1':
                    GT_rec = ((float(xmin_list[i].firstChild.data), float(ymin_list[i].firstChild.data),
                               float(xmax_list[i].firstChild.data), float(ymax_list[i].firstChild.data)))

                    # 如果找到了一个飞机目标，还需要急需往下遍历，不能跳出循环（为了防止一个图片中两个飞机）（以前是直接跳出去了）
                    plane_number += 1


                    #从DR数据表格中依次取值进行iou计算，并刷新表格
                    for i in range(len(DR_rec_list)):
                        DR_rec = (DR_rec_list[i][1],DR_rec_list[i][2],DR_rec_list[i][3],DR_rec_list[i][4])
                        if DR_rec_list[i][0] == "1" and DR_rec_list[i][6] == 0 :#先筛选出同名的类
                            iou = compute_iou(GT_rec, DR_rec)
                            if iou > 0.5 : #Iou大于0.5，则有对的可能
                                DR_rec_list[i][6] = iou
                            else:
                                DR_rec_list[i][6] = -1
                                    # plane_tp_number += 1
                    #在当前的GT框下，进行最优的预测框选取
                    iou_max = max(DR_rec_list,key= lambda x:x[6])[6]
                    for i in range(len(DR_rec_list)):
                        if DR_rec_list[i][6] != 0:
                            if DR_rec_list[i][6] == -1:
                                plane_fp_number += 1
                                DR_rec_list[i][6] == 0
                            elif DR_rec_list[i][6] == iou_max:#取最大的flag那行，tp+1，否则，flag置为0
                                plane_tp_number += 1
                            else:
                                DR_rec_list[i][6] == 0