#####################################
# 2019.7.9
# by Xinliang Zhang
# example:  python data_argument.py --ann_dir box --method vertical --img_dir ./image/
#####################################import xml.etree.ElementTree as ET
import os
from PIL import Image
###---水平镜像---###
def horizontal_ann (ann_file,img_size):# img_size (width,height)
    ann = ET.parse(ann_file)
    root = ann.getroot()
    width = img_size[0]
    height = img_size[1]
    x_min = 0
    y_min = 0
    x_max = 0
    y_max = 0
    for child in root:
        if child.tag == 'frame':
            text = child.text
            text+='_horizontal'
        if child.tag == 'object':
            for subchild in child:
                if subchild.tag == 'bndbox':
                    for subsubchild in subchild:                        
                        if subsubchild.tag=='xmin':                            
                            x_min = int(subsubchild.text)
                        elif subsubchild.tag == 'ymin':
                            y_min = int(subsubchild.text)
                            new_y_min = height - y_min
                            subsubchild.text = str(new_y_min)
                        elif subsubchild.tag == 'xmax':
                            x_max = int(subsubchild.text)
                        elif subsubchild.tag == 'ymax':
                            y_max = int(subsubchild.text)
                            new_y_max = height - y_max
                            subsubchild.text = str(new_y_max)    
    return ann

def horizontal_img(img_file):# 上下水平翻转
    img = Image.open(img_file)
    new_img = img.transpose(Image.FLIP_TOP_BOTTOM)
    return new_img
###---水平镜像---###

###---垂直镜像---###
def vertical_ann(ann_file,img_size):# 垂直左右翻转
    ann = ET.parse(ann_file)
    root = ann.getroot()
    width = img_size[0]
    height = img_size[1]
    x_min = 0
    y_min = 0
    x_max = 0
    y_max = 0
    for child in root:
        if child.tag == 'frame':
            text = child.text
            text+='_vertical'
        if child.tag == 'object':
            for subchild in child:
                if subchild.tag == 'bndbox':
                    for subsubchild in subchild:
                        if subsubchild.tag=='xmin':                            
                            x_min = int(subsubchild.text)
                            new_x_min = width - x_min
                            subsubchild.text = str(new_x_min)
                        elif subsubchild.tag == 'ymin':
                            y_min = int(subsubchild.text)                            
                        elif subsubchild.tag == 'xmax':
                            x_max = int(subsubchild.text)
                            new_x_max = width - x_max
                            subsubchild.text = str(new_x_max)
                        elif subsubchild.tag == 'ymax':
                            y_max = int(subsubchild.text)
                            
    return ann

def vertical_img(img_file):# 垂直左右翻转
    img = Image.open(img_file)
    new_img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return new_img
###---垂直镜像---###

###---旋转---###
def rotate_ann(ann_file,angle,img_size):
    ann = ET.parse(ann_file)
    root = ann.getroot()
    width = img_size[0]
    height = img_size[1]
    x_min = 0
    y_min = 0
    x_max = 0
    y_max = 0
    for child in root:
        if child.tag == 'frame':
            text = child.text
            text+='_rotate'+str(angle)
        if child.tag == 'object':
            for subchild in child:
                if subchild.tag == 'bndbox':
                    for j in range(int(angle/90)):
                        for i in range(2):
                            # 第一遍遍历，读入坐标
                            if i ==0:
                                for subsubchild in subchild:                        
                                    if subsubchild.tag=='xmin':                            
                                        x_min = int(subsubchild.text)                            
                                    elif subsubchild.tag == 'ymin':
                                        y_min = int(subsubchild.text)                            
                                    elif subsubchild.tag == 'xmax':
                                        x_max = int(subsubchild.text)                            
                                    elif subsubchild.tag == 'ymax':
                                        y_max = int(subsubchild.text)
                            #第二遍遍历，旋转坐标
                            elif i ==1:
                                for subsubchild in subchild:                        
                                    if subsubchild.tag=='xmin':                            
                                        subsubchild.text = str(height - y_max)                           
                                    elif subsubchild.tag == 'ymin':
                                        subsubchild.text = str(x_min)
                                    elif subsubchild.tag == 'xmax':
                                        subsubchild.text = str(height-y_min)     
                                    elif subsubchild.tag == 'ymax':
                                        subsubchild.text = str(x_max)
    return ann
def rotate_img(img_file,angle):
    img = Image.open(img_file)
    if angle == 90:
        new_img = img.transpose(Image.ROTATE_270)
    if angle == 180:
        new_img = img.transpose(Image.ROTATE_180)
    if angle == 270:
        new_img = img.transpose(Image.ROTATE_90)
    return new_img
###---旋转---###
