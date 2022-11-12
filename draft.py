def get_class_number(class_name,class_number,GT_dir_path):
    """
    :param class_name: 要统计的类在<category>下的名称
    :param class_number:要统计的类总的数目
    :param GT_dir_path:GT文件所在文件夹路径
    :return:class_number
    """
    # 记录文件夹下的文件数量，用于进度条
    file_number = 0
    file_all = 0

    for tag_root, tag_dirs, tags in os.walk(GT_dir_path, topdown=False):
        for tag_name in tags:
            file_all += 1
    file_all *= 1

    for tag_root, tag_dirs, tags in os.walk(GT_dir_path, topdown=False):
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
            name_list = root.getElementsByTagName('category')
            # 寻找小飞机目标
            for type_name in name_list:
                tn = type_name.firstChild.data  #记录name标签内的数据
                if tn == class_name :
                    #如果找到了一个飞机目标，就找到了一个飞机目标类的图像，无需往下遍历，跳出循环
                    class_number += 1
                    break
            change_canvas(file_number,file_all)
            return(class_number)


#====================11.01
#===========从这里开始下面需要大改

                    print(DR_rec_list)
                    #从DR数据表格中依次取值进行iou计算，大于0.5的放入iou_list,等待比较最优框（iou最大原则）
                    for i in range(len(DR_rec_list)):
                        DR_rec = (DR_rec_list[i][1],DR_rec_list[i][2],DR_rec_list[i][3],DR_rec_list[i][4])
                        #取标记为0（待测）进行比对
                        if DR_rec_list[i][6] == 0:
                            iou = compute_iou(GT_rec, DR_rec)
                            if iou > 0.5 : #iou>0.5进行进一步比对
                                if DR_rec_list[i][0] == "1": #类别对了，如果是第一次检测到，说明置信度高，此时判断它为tp，打上标记
                                    plane_tp_number += 1
                                else:

                                    iou_list.append([iou, i])
                                else:
                                    ...
                                    #问题：判断为错的识别框，还要不要和下一个GT框比较？还是要比，比如iou和当前的“1”较小，可能和下一个1较大呢

#================================================
                        #从这里开始改，先逐行判断iou，大于0.5的才进行标签的比较
                        if DR_rec_list[i][0] == "1" and DR_rec_list[i][6] == 0:#筛选同一名字的（只有同一名字才有对的可能），和flag=0的（没被检测过的框子）
                            DR_rec = (DR_rec_list[i][1],DR_rec_list[i][2],DR_rec_list[i][3],DR_rec_list[i][4])
                            iou = compute_iou(GT_rec,DR_rec)
                            if iou > 0.5:
                                iou_list.append([iou,i])   #这里出现问题，识别错误的情况没有考虑，应该是覆盖超过IOU》0.5，但是却把类别弄错了，算错的的框
                                # DR_rec_list[i][6] = 1
                    if len(iou_list) != 0:
                        iou_list.sort(key=lambda tup: tup[0])
                        # print(iou_list[-1])
                        DR_rec_list[iou_list[-1][-1]][6] = 1
                        plane_tp_number += 1

            # print(plane_fp_number)
            # print(plane_tp_number)

#问题：判断为错的识别框，还要不要和下一个GT框比较？还是要比，比如iou和当前的“1”较小，可能和下一个1较大呢


# T.insert(END, '\n"飞机"类目标共有"' + str(plane_number) + '"个，'+'所有被检测出的目标共有"'+str(plane_fp_number+plane_tp_number) + '"个，'+'其中被正确检测的目标共有"'+str(plane_tp_number) + '"个，')
# T.insert(END, '\n"该类检测的查全率为"' + str(plane_recall*100)+'%",查准率为"'+str(plane_precision*100)+'%"')
#
# T.insert(END, '\n"机场跑道"类目标共有“' + str(runway_number) + '”个，' +'所有被检测出的目标共有”' + str(runway_fp_number+runway_tp_number) + '”个，'+ '其中被正确检测的目标共有“' + str(
#     runway_tp_number) + '”个，' )
# T.insert(END, '\n"该类检测的查全率为“' + str(runway_recall) + '”,查准率为“' + str(runway_precision) + '“')
#
# T.insert(END, '\n"机场油库"类目标共有“' + str(airportOilDepot_number) + '”个，' +  '所有被检测出的目标共有”' + str(airportOilDepot_fp_number+airportOilDepot_tp_number) + '”个，'+ '其中被正确检测的目标共有“' + str(
#     airportOilDepot_tp_number) + '”个，' )
# T.insert(END, '\n"该类检测的查全率为“' + str(airportOilDepot_recall) + '”,查准率为“' + str(airportOilDepot_precision) + '“')
#
# T.insert(END, '\n"地空导弹车"类目标共有“' + str(vulcans_number) + '”个，' + '所有被检测出的目标共有”'+ str(vulcans_fp_number+vulcans_tp_number) + '”个，'+ '其中被正确检测的目标共有“' + str(
#     vulcans_tp_number) + '”个，' )
# T.insert(END, '\n"该类检测的查全率为“' + str(vulcans_recall) + '”,查准率为“' + str(vulcans_precision) + '“')

# T.insert(END, '\n"地/海面防空雷达车"类目标共有“' + str(radarVehicle_number) + '”个，' + '所有被检测出的目标共有”' + str(radarVehicle_fp_number+radarVehicle_tp_number) + '”个，'+ '其中被正确检测的目标共有“' + str(
#     radarVehicle_tp_number) + '”个，' )
# T.insert(END, '\n"该类检测的查全率为“' + str(radarVehicle_recall) + '”,查准率为“' + str(radarVehicle_precision) + '“')
# T.insert(END, '\n"桥梁"类目标共有“' + str(bridge_number) + '”个，' + '所有被检测出的目标共有”'+ str(bridge_fp_number+bridge_tp_number) + '”个，'+ '其中被正确检测的目标共有“' + str(
#     bridge_tp_number) + '”个，' )
# T.insert(END, '\n"该类检测的查全率为“' + str(bridge_recall) + '”,查准率为“' + str(bridge_precision) + '“')
# T.insert(END, '\n"运输舰艇"类目标共有“' + str(ship_number) + '”个，' + '所有被检测出的目标共有”' + str(ship_fp_number+ship_tp_number) + '”个，'+ '其中被正确检测的目标共有“' + str(
#     ship_tp_number) + '”个，' )
# T.insert(END, '\n"该类检测的查全率为“' + str(ship_recall) + '”,查准率为“' + str(ship_precision) + '“')