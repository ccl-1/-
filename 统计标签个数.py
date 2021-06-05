# -*- coding: utf-8 -*-
import os
import numpy
import shutil

def count_label(in_dir):
'''  输入： txt 文件， 格式  label  bbox'''  line 16 修改
    total = 0
    ratio = 0.0
    data_dict = {}
    data_dict_ratio= {}
    for file_name in os.listdir(in_dir):
        file_path = os.path.join(in_dir,file_name)
        for id, line in enumerate(open(file_path,'r')):
            line = line.split()
            label = line[0]  
            # 将标签和标签所对应的图片数目统计为dict格式:{label：num_label}
            if label not in data_dict:
                data_dict[label] = 0
            data_dict[label] = data_dict[label] + 1

    # 统计标签的总数目
    for val in data_dict.values():
        total += val
    print('total targer number:', total)
    
    # 计算每个标签所占的比例ratio,并将原来dict中的num_label替换为ratio,即{label:ratio}
    for key,val in data_dict.items():
        #print(val,type(val),total,type(total))
        ratio = round(float(val)/float(total),3)
        data_dict_ratio[key] = ratio

    return data_dict, data_dict_ratio


if __name__ == '__main__':

    dir = 'F:/dataset/HJJ/rssj4/科目四热身赛数据'
    in_dir = os.path.join(dir,'labelTxt')

    count_label_dict,count_label_ratio = count_label(in_dir)
    
    print('number of categories"', len(count_label_dict), '    category name:', count_label_dict.keys())
    print('count label number:', count_label_dict)
    print('count label number ratio',count_label_ratio)

