# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 19:06:50 2018

@author: 王彦欣
"""

import cv2
import numpy as np
import math



def feature_color(img_in):
    """
    输入:RGB图像
    输出：48维的向量（直方图），包含了BGR各16级的直方图信息   我试了下，性能堪忧
    """
    rows = img_in.shape[0]
    cols = img_in.shape[1]
    vec_color = np.zeros(48, 'uint32')
    for i in range(rows):
        for j in range(cols):
            b = img[i][j][0] / 16
            g = img[i][j][1] / 16
            r = img[i][j][2] / 16
            b = math.floor(b)
            g = math.floor(g)
            r = math.floor(r)
            vec_color[b * 3] += 1
            vec_color[g * 3 + 1] += 1
            vec_color[r * 3 + 2] += 1

    return vec_color



def feature_texture(img_in):
    "输入：RGB图像  ；输出：256维向量（直方图），记录LBP算法的纹理信息  性能依旧堪忧"

    vec_texture = np.zeros(256, 'uint32')
    img_gray = img_in.copy()
    img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)

    rows = img_gray.shape[0]
    cols = img_gray.shape[1]

    img_lbp = img_gray.copy()

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            current = img_gray[i][j]
            lbpcode = 0
            if current > img_gray[i - 1][j - 1]:
                lbpcode += 1
            lbpcode *= 2
            if current > img_gray[i - 1][j]:
                lbpcode += 1
            lbpcode *= 2
            if current > img_gray[i - 1][j + 1]:
                lbpcode += 1
            lbpcode *= 2
            if current > img_gray[i][j - 1]:
                lbpcode += 1
            lbpcode *= 2
            if current > img_gray[i][j + 1]:
                lbpcode += 1
            lbpcode *= 2
            if current > img_gray[i + 1][j - 1]:
                lbpcode += 1
            lbpcode *= 2
            if current > img_gray[i + 1][j]:
                lbpcode += 1
            lbpcode *= 2
            if current > img_gray[i + 1][j + 1]:
                lbpcode += 1
            img_lbp[i][j] = lbpcode

    for i in range(rows):
        for j in range(cols):
            vec_texture[img_lbp[i][j]] += 1

    return vec_texture


def feature_shape(img_in):
    "输入：RGB图像  ；输出：边缘图像（高斯滤波+Canny算子）"

    #    vec_edge=np.zeros(2,'uint32')
    img_gray = img_in.copy()
    img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)

    #    rows=img_gray.shape[0]
    #    cols=img_gray.shape[1]

    gk = cv2.getGaussianKernel(3, 0)
    img_gray = cv2.filter2D(img_gray, 0, gk)
    img_edge = cv2.Canny(img_gray, 50, 100)
    # cv2.imshow('edge', img_edge)
    # cv2.waitKey()

    #    for i in range(rows):
    #        for j in range(cols):
    #            if(img_edge[i][j]==0):
    #                vec_edge[0]+=1
    #            else:
    #                vec_edge[1]+=1
    #
    return img_edge


if __name__ == '__main__':
    import time

    img = cv2.imread("13000.jpeg")

    # cv2.imshow('test', img)
    # cv2.waitKey()
    s = time.time()
    feat_col = feature_color(img)
    feat_edge = feature_shape(img)
    feat_tex = feature_texture(img)
    print(time.time() - s)
    # print(feat_col,"\n",feat_tex,"\n",feat_edge)
