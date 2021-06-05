# encoding=utf-8

import os
import json
from PIL import Image
import numpy as np
import random

np.random.seed( 3 )
random.seed( 3 )

categories = [
    {
        "supercategory": "none",
        "id": 1,
        "name": "1"
    },{
        "supercategory": "none",
        "id": 2,
        "name": "2"
    },{
        "supercategory": "none",
        "id": 3,
        "name": "3"
    },{
        "supercategory": "none",
        "id": 4,
        "name": "4"
    },{
        "supercategory": "none",
        "id": 5,
        "name": "5"
    }
]

class_dict = {
        '1': 1,'2': 2,'3': 3,'4': 4,'5': 5
        }


def polygon_area( corners ):
    n = len( corners ) # of corners
    area = 0.0
    for i in range( n ):
        j = ( i + 1 ) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs( area ) / 2.0
    return area

_image_id = 0
_gt_id = 0

def DOTA2COCO( src, key, obj, txt_src):  # 此处的 src == dir 数据集根目录
# 4点: txt格式： ( x1 y1 x2 y2 x3 y3 x4 y4 label diff )

    global _image_id
    global _gt_id

    img_src = os.path.join( src, "images", key + ".tif" )
    width, height = Image.open( img_src ).size
    file_name = os.path.basename( img_src )
    _image_id += 1

    obj["images"].append({
        "file_name": file_name,
        "width": width,
        "height": height,
        "id": _image_id
    })

    txt_src = os.path.join( txt_src, key + ".txt" )

    if not os.path.exists( txt_src):
        return 

    with open( txt_src ) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            splits = line.split( " " )
            x1 = int( splits[0] )
            y1 = int( splits[1] )
            x2 = int( splits[2] )
            y2 = int( splits[3] )
            x3 = int( splits[4] )
            y3 = int( splits[5] )
            x4 = int( splits[6] )
            y4 = int( splits[7] )
            xmin = min( x1, x2, x3, x4 )
            xmax = max( x1, x2, x3, x4 )
            ymin = min( y1, y2, y3, y4 )
            ymax = max( y1, y2, y3, y4 )
            name = splits[8]
            diff = int( splits[9] )

            category_id = class_dict[name]
            _gt_id += 1
            segmentation = [x1, y1, x2, y2, x3, y3, x4, y4]
            corners = [( x1, y1 ), ( x4, y4 ), ( x3, y3 ), ( x2, y2 )]
            gt = {
                "ignore": diff,
                "segmentation": [segmentation],
                "area": polygon_area( corners ),
                "iscrowd": 0,
                "bbox": [xmin, ymin, xmax - xmin, ymax - ymin],
                "image_id": _image_id,
                "category_id": category_id,
                "id": _gt_id
            }

            obj["annotations"].append( gt )

def TXT2COCO( src, key, obj, txt_src):  
# 4点： txt格式： ( label x1 y1 x2 y2 x3 y3 x4 y4 ) 

    global _image_id
    global _gt_id

    img_src = os.path.join( src, "images", key + ".tif" )
    width, height = Image.open( img_src ).size
    file_name = os.path.basename( img_src )
    _image_id += 1

    obj["images"].append({
        "file_name": file_name,
        "width": width,
        "height": height,
        "id": _image_id
    })

    txt_src = os.path.join( txt_src, key + ".txt" )

    if not os.path.exists( txt_src):
        return 

    with open( txt_src ) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            splits = line.split( " " )
            x1 = int( splits[1] )
            y1 = int( splits[2] )
            x2 = int( splits[3] )
            y2 = int( splits[4] )
            x3 = int( splits[5] )
            y3 = int( splits[6] )
            x4 = int( splits[7] )
            y4 = int( splits[8] )
            xmin = min( x1, x2, x3, x4 )
            xmax = max( x1, x2, x3, x4 )
            ymin = min( y1, y2, y3, y4 )
            ymax = max( y1, y2, y3, y4 )
            name = splits[0]
            diff = 0

            category_id = class_dict[name]
            _gt_id += 1
            segmentation = [x1, y1, x2, y2, x3, y3, x4, y4]
            corners = [( x1, y1 ), ( x4, y4 ), ( x3, y3 ), ( x2, y2 )]
            gt = {
                "ignore": diff,
                "segmentation": [segmentation],
                "area": polygon_area( corners ),
                "iscrowd": 0,
                "bbox": [xmin, ymin, xmax - xmin, ymax - ymin],
                "image_id": _image_id,
                "category_id": category_id,
                "id": _gt_id
            }

            obj["annotations"].append( gt )

def convert( imagelist, src,txt_src, dst ):
    obj = {
            "images": [],
            "type": "instances",
            "annotations": [],
            "categories": categories
    }

    for k in imagelist:
        for key in imagelist[k]:
            TXT2COCO( src, key, obj, txt_src)
    with open( dst, "w" ) as f:
        json.dump( obj, f )

def collect_unaug_dataset( txtdir ):
    txts = os.listdir( txtdir )

    img_dic = {}
    for cls in class_dict:
        img_dic[cls] = []

    for txt in txts:
        dic = {}
        for cls in class_dict:
            dic[cls] = False

        with open( os.path.join( txtdir, txt ) ) as f:
            lines = f.readlines()
            for line in lines:
                # cls = line.split( " " )[-2]  # dota 数据集，label在倒数第二列
                cls = line.split( " " )[0]
                dic[cls] = True
            for key in dic:
                if dic[key]:
                    img_dic[key].append( txt[:-4] )
    return img_dic
    
 #  120 行 设置 images 路径   
 #  168 行 设置 txt 的解析方式
 #  204 行 设置 label 的读取列
dir = 'F:/dataset/HJJ/rssj4/科目四热身赛数据'  # 数据集根目录
test_ann = os.path.join( dir, "ImageSets/test" )    # 测试集的标注文件路径
train_ann = os.path.join( dir, "ImageSets/train" )  # 训练集的标注文件路径
# 生成 test.json
img_dic = collect_unaug_dataset( test_ann )  
convert( img_dic, dir, test_ann, os.path.join( dir, "ImageSets/test.json" ) )      # 第三个参数是 json 的保存路径
print("sucessfully conver test_txt to test.json")

# 生成 train.json
img_dic = collect_unaug_dataset( train_ann )  
convert( img_dic, dir, train_ann, os.path.join( dir, "ImageSets/train.json" ) )
print("sucessfully conver train_txt to train.json")




