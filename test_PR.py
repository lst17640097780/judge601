# for image_name,predict_boxes in predict_dict.items():
#     if image_name not in selected_image_name:
#         continue
#     label_boxes = label_dict[image_name]
#     for box in predict_boxes:
#         select_iou_thres = 0.5
#         box_is_ok = select_box_by_iou(box,label_boxes,select_iou_thres)
#         if box_is_ok:
#             tp_num += 1
#         else:
#             fp_num +=1
#         precision = tp_num/(tp_num+fp_num)
#         recall = tp_num/p_num


#==========================================================================
import numpy as np
# 按照置信度降序排序
sorted_ind = np.argsort(-confidence)
BB = BB[sorted_ind, :]  # 预测框坐标
image_ids = [image_ids[x] for x in sorted_ind]  # 各个预测框的对应图片id

# 便利预测框，并统计TPs和FPs
nd = len(image_ids)
tp = np.zeros(nd)
fp = np.zeros(nd)
for d in range(nd):
    R = class_recs[image_ids[d]]
    bb = BB[d, :].astype(float)
    ovmax = -np.inf
    BBGT = R['bbox'].astype(float)  # ground truth

    if BBGT.size > 0:
        # 计算IoU
        # intersection
        ixmin = np.maximum(BBGT[:, 0], bb[0])
        iymin = np.maximum(BBGT[:, 1], bb[1])
        ixmax = np.minimum(BBGT[:, 2], bb[2])
        iymax = np.minimum(BBGT[:, 3], bb[3])
        iw = np.maximum(ixmax - ixmin + 1., 0.)
        ih = np.maximum(iymax - iymin + 1., 0.)
        inters = iw * ih

        # union
        uni = ((bb[2] - bb[0] + 1.) * (bb[3] - bb[1] + 1.) +
               (BBGT[:, 2] - BBGT[:, 0] + 1.) *
               (BBGT[:, 3] - BBGT[:, 1] + 1.) - inters)

        overlaps = inters / uni
        ovmax = np.max(overlaps)
        jmax = np.argmax(overlaps)
    # 取最大的IoU
    if ovmax > 0.5:  # 是否大于阈值
        if not R['difficult'][jmax]:  # 非difficult物体
            if not R['det'][jmax]:  # 未被检测
                tp[d] = 1.
                R['det'][jmax] = 1  # 标记已被检测
            else:
                fp[d] = 1.
    else:
        fp[d] = 1.

# 计算precision recall
fp = np.cumsum(fp)
tp = np.cumsum(tp)
rec = tp / float(npos)
# avoid divide by zero in case the first detection matches a difficult
# ground truth
prec = tp / np.maximum(tp + fp, np.finfo(np.float64).eps)