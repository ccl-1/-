
# ========================= json文件，生成txt格式标注[categeries,x,y,w,h]   ==================
from __future__ import print_function
import os, sys, zipfile
import json

ann_dir='F:\\data\\fixed_annotations.json'
img_dir='F:\\data\\images'
#
def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = box[0] + box[2] / 2.0
    y = box[1] + box[3] / 2.0
    w = box[2]
    h = box[3]

    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


json_file = ann_dir  #  Object Instance 类型的标注

data = json.load(open(json_file, 'r'))

ana_txt_save_path = "./datasets/annotation"  # 保存的路径
if not os.path.exists(ana_txt_save_path):
    os.makedirs(ana_txt_save_path)

for img in data['images']:
    # print(img["file_name"])
    filename = img["file_name"]
    img_width = img["width"]
    img_height = img["height"]
    # print(img["height"])
    # print(img["width"])
    img_id = img["id"]
    ana_txt_name = filename.split(".")[0] + ".txt"  # 对应的txt名字，与jpg一致

    # 只保存图片文件名
    # with open('./datasets/train.txt', 'a+') as fp:
    #     fp.write(ana_txt_name + "\n")

    print(ana_txt_name)
    f_txt = open(os.path.join(ana_txt_save_path, ana_txt_name), 'w')
    for ann in data['annotations']:
        if ann['image_id'] == img_id:
            # annotation.append(ann)
            # print(ann["category_id"], ann["bbox"])
            box = convert((img_width, img_height), ann["bbox"])
            f_txt.write("%s %s %s %s %s\n" % (ann["category_id"], box[0], box[1], box[2], box[3]))
    f_txt.close()









# # json转换成txt文件. x_min, y_min, x_max, y_max, int(info[1])

# import json
# import os
# from collections import defaultdict
# from pycocotools.coco import COCO
#
# ann_dir='F:\\瓶装白酒疵品质检\\chongqing1_round1_train1_20191223\\fixed_annotations.json'
# img_dir='F:\\瓶装白酒疵品质检\\chongqing1_round1_train1_20191223\\images'
#
# name_box_id = defaultdict(list)
# id_name = dict()
# f = open(ann_dir,encoding='utf-8')
# data = json.load(f)
# annotations = data['annotations']
#
# coco = COCO(ann_dir)
# img_id = coco.getImgIds()
#
#
# for ant in annotations:
#     id = ant['image_id']
#     img_detail = coco.loadImgs(ids=[id])
#     img_path = os.path.join(img_detail[0]['file_name']).strip()
#     name = './datasets/restricted/%d.jpg' % id
#     cat = ant['category_id']
#     name_box_id[img_path].append([ant['bbox'], cat])
#
#     # name_box_id[name].append([ant['bbox'], cat])
#
# f = open('./datasets/train.txt', 'w')
# for key in name_box_id.keys():
#     f.write(key)
#     box_infos = name_box_id[key]
#     for info in box_infos:
#         x_min = int(info[0][0])
#         y_min = int(info[0][1])
#         x_max = x_min + int(info[0][2])
#         y_max = y_min + int(info[0][3])
#
#         box_info = " %d,%d,%d,%d,%d" % (
#             x_min, y_min, x_max, y_max, int(info[1]))
#         f.write(box_info)
#     f.write('\n')
# f.close()
#
# img_detail = coco.loadImgs(ids=[1])
# img_path = os.path.join(img_detail[0]['file_name']).strip()
# print(img_path)