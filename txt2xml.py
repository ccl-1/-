# coding: utf-8
from lxml.etree import Element,SubElement,tostring
from xml.dom.minidom import parseString
import xml.dom.minidom
import os
import sys
from PIL import Image
import cv2 as cv


'''
readtxt_p2, readtxt_p4 : 读取 txt 文本
deal_p2, deal_p4: 把 txt 中的内容写进xml
writexml_p2, writexml_p4:  创建xml文件
p2 ,p4 分别对应 二点矩形框 和 四点 旋转矩形框

'''

# 读取图像 h，w
def readsize(filename):  
    img = Image.open(img_path + '/' + filename)
    width = img.size[0]
    height = img.size[1]    
    return height,width

# 二点坐标: label x1 y1 x2 y2  （左上角， 右下角）
def readtxt_p2(path):
    with open(path,'r') as f:
        contents = f.read()
        objects = contents.split('\n')#分割出每个物体
        for i in range(objects.count('')):#去掉空格项， 换行符
           objects.remove('')
        num = len(objects) # 一张图片中，目标的数量
        print(objects,num)
        xmins, ymins, xmaxs, ymaxs, names = [], [], [], [], [], []

        for line in objects:
            line = line.strip().split(' ')
            name = line[0]  #  label
            x1 = int(line[1]);  y1 = int(line[2])
            x2 = int(line[3]);  y2 = int(line[4])

            xmins.append(xmin), ymins.append(ymin)
            xmaxs.append(xmax), ymaxs.append(ymax)
            names.append(name)
        
        return num,names,  xmins, ymins, xmaxs, ymaxs

# 四点坐标:  label x1 y1 x2 y2 x3 y3 x4 y4 
def readtxt_p4(path):
    with open(path,'r') as f:
        contents = f.read()

        objects = contents.split('\n')#分割出每个物体
        for i in range(objects.count('')):#去掉空格项， 换行符
           objects.remove('')
        num = len(objects) # 一张图片中，目标的数量
        print(objects,num)
        x1, y1, x2, y2, x3, y3, x4, y4, names = [], [], [], [], [], [], [], [], []

        for line in objects:
            line = line.strip().split(' ')
            name = line[0]  #  label
            _x1 = int(line[1]);  _y1 = int(line[2])
            _x2 = int(line[3]);  _y2 = int(line[4])
            _x3 = int(line[5]);  _y3 = int(line[6])
            _x4 = int(line[7]);  _y4 = int(line[8]) 

            x1.append(_x1), y1.append(_y1)
            x2.append(_x2), y2.append(_y2)
            x3.append(_x3), y3.append(_y3)
            x4.append(_x4), y4.append(_y4)
            names.append(name)
        
        return num,names, x1,y1,x2,y2,x3,y3,x4,y4


# 把 txt 中的内容写进xml
# 二点坐标 
def deal_p2(txt_path,xml_path):
    files = os.listdir(txt_path)#列出所有文件
    for file in files:
        filename = os.path.splitext(file)[0] #分割出所有不带后缀的文件名
        sufix = os.path.splitext(file)[1] #分割出后缀
        if sufix =='.txt':
            num,names,  xmins, ymins, xmaxs, ymaxs= readtxt_p2(txt_path+'/'+file)
            dealpath = xml_path + "/"+ filename + ".xml"
            filename = filename + '.tif'    
            with open(dealpath,'w') as f:
                writexml_p2(dealpath,filename,num,names,  xmins, ymins, xmaxs, ymaxs)
        print('convert {}sucessfully' .format(file))

# 四点坐标
def deal_p4(txt_path,xml_path):
    files = os.listdir(txt_path)#列出所有文件
    for file in files:
        filename = os.path.splitext(file)[0] #分割出所有不带后缀的文件名
        sufix = os.path.splitext(file)[1] #分割出后缀
        if sufix =='.txt':
            num, names, x1,y1,x2,y2,x3,y3,x4,y4 = readtxt_p4(txt_path+'/'+file)
            dealpath = xml_path + "/"+ filename + ".xml"
            filename = filename + '.tif'    
            with open(dealpath,'w') as f:
                writexml_p4(dealpath,filename,num, names, x1,y1,x2,y2,x3,y3,x4,y4)
        print('convert {}sucessfully' .format(file))



# 创建xml文件
# 2点
def writexml_p2(path,filename,num,names,  xmins, ymins, xmaxs, ymaxs): 

    height, width = readsize(filename)

    node_root=Element('annotation')

    node_folder=SubElement(node_root,'folder')
    node_folder.text="VOC2007"

    node_filename=SubElement(node_root,'filename')
    node_filename.text="%s" % filename

    node_size=SubElement(node_root,"size")
    node_width = SubElement(node_size, 'width')
    node_width.text = '%s' % width

    node_height = SubElement(node_size, 'height')
    node_height.text = '%s' % height

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '3'
    for i in range(num):
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        node_name.text = '%s' % names[i]

        node_name = SubElement(node_object, 'pose')
        node_name.text = '%s' % "unspecified"
        node_name = SubElement(node_object, 'truncated')
        node_name.text = '%s' % "0"
        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'

        node_bndbox = SubElement(node_object, 'bndbox')     
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = '%s'% xmins[i]
        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = '%s' % ymins[i]
        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = '%s' % xmaxs[i]
        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = '%s' % ymaxs[i]

    xml = tostring(node_root, pretty_print=True)  
    dom = parseString(xml)
    with open(path, 'wb') as f:
        f.write(xml)
    return

# 4点
def writexml_p4(path,filename,num, names, x1,y1,x2,y2,x3,y3,x4,y4): 

    height, width = readsize(filename)

    node_root=Element('annotation')

    node_folder=SubElement(node_root,'folder')
    node_folder.text="VOC2007"

    node_filename=SubElement(node_root,'filename')
    node_filename.text="%s" % filename

    node_size=SubElement(node_root,"size")
    node_width = SubElement(node_size, 'width')
    node_width.text = '%s' % width

    node_height = SubElement(node_size, 'height')
    node_height.text = '%s' % height

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '3'
    for i in range(num):
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        node_name.text = '%s' % names[i]

        node_name = SubElement(node_object, 'pose')
        node_name.text = '%s' % "unspecified"
        node_name = SubElement(node_object, 'truncated')
        node_name.text = '%s' % "0"
        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'

        node_bndbox = SubElement(node_object, 'bndbox')
        node_x1 = SubElement(node_bndbox, 'x1')
        node_x1.text = '%s'% x1[i]
        node_y1 = SubElement(node_bndbox, 'y1')
        node_y1.text = '%s' % y1[i]

        node_x2 = SubElement(node_bndbox, 'x2')
        node_x2.text = '%s' % x2[i]
        node_y2 = SubElement(node_bndbox, 'y2')
        node_y2.text = '%s' % y2[i]

        node_x3 = SubElement(node_bndbox, 'x3')
        node_x3.text = '%s' % x3[i]
        node_y3 = SubElement(node_bndbox, 'y3')
        node_y3.text = '%s' % y3[i]

        node_x4 = SubElement(node_bndbox, 'x4')
        node_x4.text = '%s' % x4[i]
        node_y4 = SubElement(node_bndbox, 'y4')
        node_y4.text = '%s' % y4[i]

    xml = tostring(node_root, pretty_print=True)  
    dom = parseString(xml)
    with open(path, 'wb') as f:
        f.write(xml)
    return


if __name__ == "__main__":

    dir = "F:/dataset/HJJ/rssj4/科目四热身赛数据"
    txt_path = os.path.join(dir, "labelTxt")
    img_path = os.path.join(dir, "images")
    xml_path = os.path.join(dir, "labels")

    deal_p4(txt_path,xml_path)      #  把txt中的内容写进xml  四点坐标
    #deal_p2(txt_path,xml_path)     # 二点坐标



