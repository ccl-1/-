#!/usr/bin/env python
# coding: utf-8

from PIL import Image,ImageFilter,ImageDraw,ImageFont
from itertools import groupby
import numpy as np
import shutil
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
import random
import os
import sys
import json
import cv2 as cv


def parse_voc_p2(xml_path): 
""" 解析读取xml函数: Parse a PASCAL VOC xml file """
    tree = ET.parse(xml_path)
    objects = []
    img_dir =[]
    for xml_name in tree.findall('filename'):
        img_path = os.path.join(pic_path, xml_name.text)
        img_dir.append(img_path)
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        obj_struct['pose'] = obj.find('pose').text
        obj_struct['truncated'] = int(obj.find('truncated').text)
        obj_struct['difficult'] = int(obj.find('difficult').text)
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text),
                              int(bbox.find('ymin').text),
                              int(bbox.find('xmax').text),
                              int(bbox.find('ymax').text)]
        objects.append(obj_struct)
    return objects,img_dir

def parse_gt_txt(txt_path):
'''标注格式： label x1 y1 x2 y2 x3 y3 x4 y4  '''
    
    objects = []
    for id, line in enumerate(open(txt_path,'r')):
        obj_struct = {}
        line = line.split(' ')
        name = line[0]
        x1 = int(line[1]);  y1 = int(line[2])
        x2 = int(line[3]);  y2 = int(line[4])
        x3 = int(line[5]);  y3 = int(line[6])
        x4 = int(line[7]);  y4 = int(line[8])  
        #print(x1,y1,x2,y2,x3,y3,x4,y4)
        
        a = ((x2-x1) * (x2-x1) + (y2-y1) * (y2-y1)) ** 0.5
        b = ((x4-x1) * (x4-x1) + (y1-y4) * (y1-y4)) ** 0.5
        area = int(a * b)
        
        obj_struct['name'] = name
        obj_struct['bbox'] = [x1,y1,x2,y2,x3,y3,x4,y4]
        obj_struct['area'] = area
        objects.append(obj_struct)
    return objects
    
def parse_txt(txt_path):
''' 标注格式：label score x1 y1 x2 y2 x3 y3 x4 y4 '''
    
    objects = []
    for id, line in enumerate(open(txt_path,'r')):
        obj_struct = {}
        line = line.split(' ')
        name = line[0]
        x1 = int(line[2]);  y1 = int(line[3])
        x2 = int(line[4]);  y2 = int(line[5])
        x3 = int(line[6]);  y3 = int(line[7])
        x4 = int(line[8]);  y4 = int(line[9])  

        a = ((x2-x1) * (x2-x1) + (y2-y1) * (y2-y1)) ** 0.5
        b = ((x4-x1) * (x4-x1) + (y1-y4) * (y1-y4)) ** 0.5
        area = int(a * b)
        
        obj_struct['name'] = name
        obj_struct['bbox'] = [x1,y1,x2,y2,x3,y3,x4,y4]
        obj_struct['area'] = area
        objects.append(obj_struct)
    return objects


# 可视化函数-> input：图片路径
def visualise_p4(objects, img_path):
''' 4点坐标：x1 y1 x2 y2 x3 y3 x4 y4  '''
    img = Image.open(img_path)
    img = img.convert('RGB')      #   若不转换，后面绘制矩形框的时候，边框颜色只能设置一位数（灰度值），
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('mvboli.ttf', 30)
    for a in objects:
        label = a['name']
        bbox = a['bbox']
        x1 = int(bbox[0]);  y1 = int(bbox[1])
        x2 = int(bbox[2]);  y2 = int(bbox[3])
        x3 = int(bbox[4]);  y3 = int(bbox[5])
        x4 = int(bbox[6]);  y4 = int(bbox[7]) 

        draw.line([(x1,y1), (x2,y2), (x3,y3), (x4,y4),(x1,y1)], fill=(255,0,0), width=3)
        draw.text((max(0,x1-40),max(0,y1-40)),  label, fill = (0, 255, 0),font = font)
    
    # plt.figure(figsize=(10,10),dpi=80)
    
    plt.figure()
    plt.imshow(img)
    plt.title(img_path)
    plt.show()

def visualise_p2(objects, img_path):
'''  2点坐标：x1 y1 x2 y2  '''
    img = cv.imread(img_path)

    for a in objects:
        label = a['name']
        bbox = a['bbox']
        x1 = int(bbox[0]);  y1 = int(bbox[1])
        x2 = int(bbox[2]);  y2 = int(bbox[3])
        cv.rectangle(img, (x1,y1), (x2,y2), (255,0,0),2) 
        cv.putText(img, label, (max(0,x1-10),max(0,y1-10)), Font, 10, (255,0,0), 2)  
        #cv2.putText(img, text, (x,y), Font, Size, (B,G,R), Thickness)
    
    plt.figure(figsize=(10,10),dpi=80)
    plt.imshow(img)
    plt.title(img_path)
    plt.show()


def visualise_compare(objects, gt_objects, img_path):
''' 预测与真值对比函数  '''
   
    img = Image.open(img_path)
    img = img.convert('RGB')      #   若不转换，后面绘制矩形框的时候，边框颜色只能设置一位数（灰度值），
    draw = ImageDraw.Draw(img)

    for a in objects:
        label = a['name']
        bbox = a['bbox']
        x1 = int(bbox[0]);  y1 = int(bbox[1])
        x2 = int(bbox[2]);  y2 = int(bbox[3])
        x3 = int(bbox[4]);  y3 = int(bbox[5])
        x4 = int(bbox[6]);  y4 = int(bbox[7]) 
        draw.line([(x1,y1), (x2,y2), (x3,y3), (x4,y4),(x1,y1)], fill=(255,0,0), width=3)
        
    for a in gt_objects:
        label = a['name']
        bbox = a['bbox']
        x1 = int(bbox[0]);  y1 = int(bbox[1])
        x2 = int(bbox[2]);  y2 = int(bbox[3])
        x3 = int(bbox[4]);  y3 = int(bbox[5])
        x4 = int(bbox[6]);  y4 = int(bbox[7]) 
        draw.line([(x1,y1), (x2,y2), (x3,y3), (x4,y4),(x1,y1)], fill=(0,255,0), width=3)

    plt.figure(figsize=(10,10),dpi=80)
    plt.imshow(img)
    plt.title(img_path)
    plt.xlabel("red bbox: pre-bbox,   green bbox: ground_truth bbox")

    plt.show()

if __name__ == "__main__":

    dir = "F:/dataset/HJJ/rssj4/科目四热身赛数据"   
    gt_dir = os.path.join(dir, 'labelTxt')  # 真值路径
    img_dir = os.path.join(dir, "images")  # 图像路径
    pre_dir = os.path.join(dir, "results") # 预测结果路径

    for filename in os.listdir(gt_dir):

        img_path = os.path.join(img_dir,filename.split('.txt')[0]+".tif")
        
        # 预测
        #pre_path = os.path.join(pre_dir,filename)         # 标注文件路径 
        #objects = parse_txt(pre_path)      # 标注文件 解析，得到的 objects 包含一副图像中 所有的目标bbox信息
        
        # 真值
        gt_path = os.path.join(gt_dir,filename)
        gt_objects = parse_gt_txt(gt_path)
        
        # 可视化
        visualise_p4(gt_objects, img_path) 
        # 可视化对比
        #visualise_compare(objects,gt_objects, img_path) 
        
        


