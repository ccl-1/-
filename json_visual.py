'''
from pycocotools.coco import COCO
import os
import shutil
from tqdm import tqdm
import matplotlib.pyplot as plt
import cv2
from PIL import Image, ImageDraw, ImageFont
import argparse
 
def id2name(coco):
    classes=dict()
    for cls in coco.dataset['categories']:
        classes[cls['id']]=cls['name']
    return classes

def parse_json(coco, img_id, cls_map, cls_ids):
    annIds = coco.getAnnIds(imgIds = [img_id], catIds = cls_ids, iscrowd = None)
    anns = coco.loadAnns(annIds)
    objects = []
    for ann in anns:
        obj_struct = {}
        image_id = ann['image_id']  # 与 images 的 id 对应，找到 file_name
        cls_id = ann['category_id']
        if cls_id in cls_ids and 'bbox' in ann:
            bbox = ann['bbox']
            xmin = int(bbox[0])
            ymin = int(bbox[1])
            xmax = int(bbox[2] + bbox[0])
            ymax = int(bbox[3] + bbox[1])

            point = ann['segmentation'][0]
            x1 = int(point[0])
            y1 = int(point[1])
            x2 = int(point[2])
            y2 = int(point[3])
            x3 = int(point[4])
            y3 = int(point[5])
            x4 = int(point[6])
            y4 = int(point[7])
            obj_struct['segmentation'] = [x1, y1, x2, y2, x3, y3, x4, y4]

            obj_struct['image_id'] = image_id
            obj_struct['name'] = cls_id  # 可以在这里设置 映射
            obj_struct['area'] = ann['area']
            obj_struct['bbox'] = [xmin,ymin,xmax,ymax]

            objects.append(obj_struct) 

    return objects
 

def visualise_p4(objects, img_path):
    # 4点坐标：x1 y1 x2 y2 x3 y3 x4 y4 
    img = Image.open(img_path)
    img = img.convert('RGB')      #   若不转换，后面绘制矩形框的时候，边框颜色只能设置一位数（灰度值），
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('mvboli.ttf', 30)
    for a in objects:
        label = a['name']
        bbox = a['segmentation']
        x1 = int(bbox[0]);  y1 = int(bbox[1])
        x2 = int(bbox[2]);  y2 = int(bbox[3])
        x3 = int(bbox[4]);  y3 = int(bbox[5])
        x4 = int(bbox[6]);  y4 = int(bbox[7]) 
        #print(x1,y1,x2,y2,x3,y3,x4,y4)
        draw.line([(x1,y1), (x2,y2), (x3,y3), (x4,y4),(x1,y1)], fill=(255,0,0), width=3)
        #draw.text((max(0,x1-40),max(0,y1-40)),  label, fill = (0, 255, 0),font = font)    
    plt.figure()
    plt.imshow(img)
    plt.title(img_path)
    plt.show()

if __name__ == "__main__":

    root = 'F:/dataset/HJJ/rssj4/科目四热身赛数据/'
    input_dir = os.path.join(root, 'ImageSets/test.json')

    coco = COCO(input_dir)
    cat = coco.loadCats(coco.getCatIds())

    cls_map = id2name(coco)
    cls_ids = coco.getCatIds()

    img_ids = []
    for cls_id in cls_ids:
        img_ids.extend(coco.getImgIds(catIds = cls_id))
    #img_ids = set(img_ids)
    print("image ids:", len(img_ids))

    for imgId in img_ids:
        img = coco.loadImgs(imgId)
        filename = img[0]['file_name']
        img_id = img[0]['id']
        objects = parse_json(coco, img_id, cls_map, cls_ids)
        img_path = os.path.join(root, 'images', filename)
        visualise_p4(objects, img_path)
        #print(objs)
'''

    
from pycocotools.coco import COCO
import skimage.io as io
import matplotlib.pyplot as plt
import pylab, os, cv2, shutil
import os.path as osp
import numpy as np
from PIL import Image,ImageFilter,ImageDraw,ImageFont

coco_classes = ['1', '2', '3', '4', '5']
SelectedCats = ['1', '2', '3', '4', '5']

def show_cv(coco, img_prefix, img, classes, SelectedCats=None):
    img_path = os.path.join(img_prefix,img['file_name'])
    I= cv2.imread(img_path)
    '''I = Image.open(img_path)
    I = I.convert('RGB')  
    draw = ImageDraw.Draw(I)
    font = ImageFont.truetype('mvboli.ttf', 30)
    '''
    annIds = coco.getAnnIds(imgIds=img['id'], iscrowd=None)
    anns = coco.loadAnns(annIds)
    objs = []
    for ann in anns:
        name = classes[ann['category_id']]
        if name in SelectedCats:
            if 'segmentation' in ann:
                point = ann['segmentation'][0]
                x1 = int(point[0]);  y1 = int(point[1])
                x2 = int(point[2]);  y2 = int(point[3])
                x3 = int(point[4]);  y3 = int(point[5])
                x4 = int(point[6]);  y4 = int(point[7]) 
                obj = [name,x1,y1,x2,y2,x3,y3,x4,y4]
                objs.append(obj)

                pts = np.array([[x1,y1],[x2,y2],[x3,y3],[x4,y4],[x1,y1]],np.int32) #数据类型必须是int32
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(I, [pts], True,(0,255,0),2)
                
    cv2.namedWindow(img_path, 0)
    cv2.resizeWindow(img_path, 600, 500)
    cv2.imshow(img_path, I)
    cv2.waitKey(0) #0表示等待键盘按键
    
   

def catid2name(coco):
    classes = dict()
    for cat in coco.dataset['categories']:
        classes[cat['id']] = cat['name']
        # print(str(cat['id'])+":"+cat['name'])
    return classes

if __name__=="__main__":

    root = 'F:/dataset/HJJ/rssj4/data/'
    annFile = os.path.join(root, 'ImageSets/test.json') 
    img_prefix =os.path.join(root, 'images')

    coco = COCO(annFile)
    coco_catid2name = catid2name(coco)
    fig = plt.figure()
    plt.ion()  # matplotlib interactivate mode 当交互模式打开后，plt.show()不会阻断运行
    for img_id in coco.imgs:
        img=coco.imgs[img_id]
        # 通多opencv交互显示图像和标注；按下键盘回车或者空格自动显示下一张图像
        show_cv(coco,img_prefix,img,coco_catid2name,SelectedCats) 
        # 通过matplotlib.pylot交互显示图像和标注；点击鼠标或者键盘自动显示下一张图像
        # show_plt(coco, img_prefix, img, coco_catid2name, SelectedCats,fig=fig)
