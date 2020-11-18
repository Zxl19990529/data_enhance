#####################################
# 2020.11.18
# by Xinliang Zhang
# example:  python vis_xml_bbox.py --ann_dir box/ --img_dir image/
#####################################
from PIL import Image,ImageDraw
import os
import numpy as  np 
import xml.etree.ElementTree as ET 
import argparse
from multiprocessing import Pool
from tqdm import tqdm
import math
parser = argparse.ArgumentParser()
parser.add_argument('--ann_dir',type=str,default='box',help="Direction to annotation files.")
parser.add_argument('--img_dir',type=str,default='image',help='Direction to JPEGImage files.')
parser.add_argument('--save_dir',type=str,default='visualized',help='Direction to save the visualized images.')
parser.add_argument('--kernels',type=int,default=8,help="Use multiple kernel to accerate the processing")
args = parser.parse_args()


def get_bbox(tree):
    root = tree.getroot()
    result = []
    for child in root:
        if child.tag == 'object':
            name = ''
            pt = []
            for subchild in child:
                if subchild.tag == 'name':
                    name = subchild.text
                    # print(name)# holothurian
                if subchild.tag == 'bndbox':
                    for subsub_child in subchild:
                        pt.append(int(subsub_child.text))
            # print(pt)# [642, 412, 757, 524]  [x_min,y_min,x_max,y_max]
            result.append([name,pt])
        else:
            continue
    return result
def cut_by_kernels(total_file_list,kernels):
    cut_results = []
    stride = math.ceil(len(total_file_list)/kernels)
    print(stride)
    for i in range(kernels):
        tmp = total_file_list[i*stride:i*stride+stride]
        start = tmp[0]
        end = tmp[-1]
        cut_results.append(tmp)
    return cut_results

def draw_images(ann_list,kernel_id):
    pbar = tqdm(ann_list,position=kernel_id)
    for filename in ann_list:
        pbar.update(1)
        base_name = filename.split('.')[0]
        xml_file = os.path.join(ann_dir,filename)
        tree = ET.parse(xml_file)
        result = get_bbox(tree)
        img = os.path.join(img_dir,base_name+'.jpg')
        img = Image.open(img)
        draw = ImageDraw.Draw(img)
        for target in result:
            text = target[0]
            pt = target[1]
            x1,y1,x2,y2 = pt[0],pt[1],pt[2],pt[3]
            draw.rectangle((x1,y1,x2,y2), width=2)   # width=3时 比较粗
            draw.text((x1,y1),text)
        img.save(os.path.join(save_dir,base_name+'.jpg'))

if __name__ == "__main__":
    kernels = args.kernels
    save_dir = args.save_dir
    ann_dir = args.ann_dir
    img_dir = args.img_dir
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    total_ann_files = sorted(os.listdir(ann_dir))
    cut_slices = cut_by_kernels(total_ann_files,kernels)
    pol = Pool(kernels)
    for i,ann_list in enumerate(cut_slices):
        pol.apply_async(draw_images,(ann_list,i))
    pol.close()
    pol.join()
    # for i,ann_list in enumerate(cut_slices):
    #     draw_images(cut_slices[i+1],i+1)


# total_ann_filename = os.listdir(ann_dir)

# for filename in os.listdir(ann_dir):
#     amount = len(os.listdir(ann_dir))
#     base_name = filename.split('.')[0]
#     xml_file = os.path.join(ann_dir,filename)
#     tree = ET.parse(xml_file)
#     result = get_bbox(tree)
#     # print(result)
#     img = os.path.join(img_dir,base_name+'.jpg')
#     img = Image.open(img)
#     # img.show()
#     # break
#     draw = ImageDraw.Draw(img)
#     for target in result:
#         text = target[0]
#         pt = target[1]
#         x1,y1,x2,y2 = pt[0],pt[1],pt[2],pt[3]
#         # draw.rectangle((x1,y1,x2,y2))
#         # 增宽线条宽度
#         draw.rectangle((x1,y1,x2,y2), width=2)   # width=3时 比较粗
#         draw.text((x1,y1),text)
#     img.save(os.path.join(save_dir,base_name+'.jpg'))
