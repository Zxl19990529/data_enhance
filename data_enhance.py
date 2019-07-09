#####################################
# 2019.7.9
# by Xinliang Zhang
# example:  python data_argument.py --ann_dir box --method vertical --img_dir ./image/
#####################################
import os
import xml.etree.ElementTree as ET
import argparse
import numpy as np
from PIL import Image
from utils import*
parser = argparse.ArgumentParser()

parser.add_argument('--img_dir', type=str, default='JPEGImages',
                    help='The direction to Image files')
parser.add_argument('--ann_dir', type=str, default='Annotations',
                    help='The direction to annotations files')
parser.add_argument('--method', type=str,
                    help='The method of data argumentation, including horizontal(水平翻转),vertical（垂直翻转）,rotate(顺时针旋转)')
parser.add_argument('--angle', type=int, default=90,
                    help='If the method is rotate, the angle is needed')
                    
args = parser.parse_args()

ann_files = os.listdir(args.ann_dir)
# print(ann_files)
img_files = os.listdir(args.img_dir)
img_save_dir = './img_'+args.method
ann_save_dir = './ann_'+args.method
if args.method == 'rotate':
    img_save_dir += '_'+str(args.angle)
    ann_save_dir += '_'+str(args.angle)
if not os.path.exists(ann_save_dir):
    os.mkdir(ann_save_dir)
if not os.path.exists(img_save_dir):
    os.mkdir(img_save_dir)

if args.method == 'horizontal':
    for ann_file in ann_files:
        basename = ann_file.split('.')[0]
        img_name = basename+'.jpg'
        ann_file = os.path.join(args.ann_dir, ann_file)
        img_file = os.path.join(args.img_dir, img_name)
        # print(img_file)
        img = Image.open(img_file)

        ann_horizontal = horizontal_ann(ann_file,img.size)
        img_horizontal = horizontal_img(img_file)

        ann_horizontal.write(os.path.join(ann_save_dir,basename+'_horizontal.xml'))
        print(os.path.join(ann_save_dir,basename+'_horizontal.xml'))
        img_horizontal.save(os.path.join(img_save_dir,basename+'_horizontal.jpg'))
        print(os.path.join(img_save_dir,basename+'_horizontal.jpg'))
if args.method == 'vertical':
    for ann_file in ann_files:
        basename = ann_file.split('.')[0]
        img_name = basename+'.jpg'
        ann_file = os.path.join(args.ann_dir, ann_file)
        img_file = os.path.join(args.img_dir, img_name)
        # print(img_file)
        img = Image.open(img_file)

        ann_vertical = vertical_ann(ann_file,img.size)
        img_vertical = vertical_img(img_file)

        ann_vertical.write(os.path.join(ann_save_dir,basename+'_vertical.xml'))
        print(os.path.join(ann_save_dir,basename+'_vertical.xml'))
        img_vertical.save(os.path.join(img_save_dir,basename+'_vertical.jpg'))
        print(os.path.join(img_save_dir,basename+'_vertical.jpg'))

if args.method == 'rotate':
    angle = args.angle
    for ann_file in ann_files:
        basename = ann_file.split('.')[0]
        img_name = basename+'.jpg'
        ann_file = os.path.join(args.ann_dir, ann_file)
        img_file = os.path.join(args.img_dir, img_name)
        # print(img_file)
        img = Image.open(img_file)

        ann_rotated = rotate_ann(ann_file,angle,img.size)
        img_rotated = rotate_img(img_file,angle)

        ann_rotated.write(os.path.join(ann_save_dir,basename+'_rotate_'+str(angle))+'.xml')
        print(os.path.join(ann_save_dir,basename+'_rotate_'+str(angle)+'.xml'))
        img_rotated.save(os.path.join(img_save_dir,basename+'_rotate_'+str(angle)+'.jpg'))
        print(os.path.join(img_save_dir,basename+'_rotate_'+str(angle)+'.jpg'))