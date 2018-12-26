import math
from skimage import io, color
import numpy as np

import cv2
import time

from colormath.color_objects import LabColor
from colormath.color_diff import delta_e_cie2000

class Cluster(object):
    cluster_index = 1

    def __init__(self, h, w, l=0, a=0, b=0):
        self.update(h, w, l, a, b)
        self.pixels = {}
        self.no = self.cluster_index
        Cluster.cluster_index += 1

    def update(self, h, w, l, a, b):
        self.h = h
        self.w = w
        self.l = l
        self.a = a
        self.b = b

class SLICProcessor(object):
    @staticmethod
    def open_image(path):
        """
        Return:
            3D array, row col [LAB]
        """
        rgb = io.imread(path)
        lab_arr = color.rgb2lab(rgb)
        # rgb = cv2.imread(path)
        # lab_arr = cv2.cvtColor(rgb,cv2.COLOR_RGB2LAB)
        return lab_arr

    @staticmethod
    def save_lab_image(path, lab_arr):
        """
        Convert the array to RBG, then save the image
        :param path:
        :param lab_arr:
        :return:
        """
        rgb_arr = color.lab2rgb(lab_arr)
        io.imsave(path, rgb_arr)
        # bgr_arr=cv2.cvtColor(lab_arr,cv2.COLOR_LAB2BGR)
        # cv2.imwrite(path,bgr_arr)

    def make_cluster(self, h, w):
        h=int(h)
        w=int(w)
        return Cluster(h, w,
                       self.data[h][w][0],
                       self.data[h][w][1],
                       self.data[h][w][2])

    def __init__(self, filename, K, M=30):
        self.K = K
        self.M = M

        self.data = self.open_image(filename)
        self.image_height = self.data.shape[0]
        self.image_width = self.data.shape[1]
        self.N = self.image_height * self.image_width
        self.S = int(math.sqrt(self.N / self.K))

        self.clusters = []
        self.label = {}
        self.dis = np.full((self.image_height, self.image_width), np.inf)

    def init_clusters(self):
        """
        初始化聚类，等分布撒聚类初始点
        """
        h = self.S / 2
        w = self.S / 2
        while h < self.image_height:
            while w < self.image_width:
                self.clusters.append(self.make_cluster(h, w))
                w += self.S
            w = self.S / 2
            h += self.S

    def get_gradient(self, h, w):
        '''
        获得点与它主对角线点的梯度
        '''
        if w + 1 >= self.image_width:
            w = self.image_width - 2
        if h + 1 >= self.image_height:
            h = self.image_height - 2

        gradient = self.data[h + 1][w + 1][0] - self.data[h][w][0] + \
                   self.data[h + 1][w + 1][1] - self.data[h][w][1] + \
                   self.data[h + 1][w + 1][2] - self.data[h][w][2]
        return gradient

    def move_clusters(self):
        '''
        取当前聚类点的领域点中，梯度最小的点作为聚类中心点
        '''
        for cluster in self.clusters:
            cluster_gradient = self.get_gradient(cluster.h, cluster.w)
            for dh in range(-1, 2):
                for dw in range(-1, 2):
                    _h = cluster.h + dh
                    _w = cluster.w + dw
                    new_gradient = self.get_gradient(_h, _w)
                    if new_gradient < cluster_gradient:
                        cluster.update(_h, _w, self.data[_h][_w][0], self.data[_h][_w][1], self.data[_h][_w][2])
                        cluster_gradient = new_gradient

    def assignment(self):
        '''
        将图像中的每一个点划分到距离它最近的聚类中
        '''
        l=len(self.clusters)
        count=0
        for cluster in self.clusters:
            # print('%.2f'%(count/l))
            count+=1
            for h in range(cluster.h - 2 * self.S, cluster.h + 2 * self.S):
                if h < 0 or h >= self.image_height: continue
                for w in range(cluster.w - 2 * self.S, cluster.w + 2 * self.S):
                    if w < 0 or w >= self.image_width: continue
                    L, A, B = self.data[h][w]
                    Dc = math.sqrt(
                        math.pow(L - cluster.l, 2) +
                        math.pow(A - cluster.a, 2) +
                        math.pow(B - cluster.b, 2))
                    Ds = math.sqrt(
                        math.pow(h - cluster.h, 2) +
                        math.pow(w - cluster.w, 2))
                    D = math.sqrt(math.pow(Dc / self.M, 2) + math.pow(Ds / self.S, 2))
                    if D < self.dis[h][w]:
                        if (h, w) not in self.label:
                            self.label[(h, w)] = cluster
                            cluster.pixels[(h, w)]=1
                        else:
                            self.label[(h, w)].pixels[(h,w)]=0
                            self.label[(h, w)] = cluster
                            cluster.pixels[(h,w)]=1
                        self.dis[h][w] = D

    def update_cluster(self):
        '''
        取聚类中所有点的平均位置作为聚类的中心点
        :return:
        '''
        for cluster in self.clusters:
            sum_h = sum_w = number = 0
            for p in cluster.pixels.keys():
                if(cluster.pixels[p]==0):
                    continue
                sum_h += p[0]
                sum_w += p[1]
                number += 1
                _h = int(sum_h / number)
                _w = int(sum_w / number)
                cluster.update(_h, _w, self.data[_h][_w][0], self.data[_h][_w][1], self.data[_h][_w][2])

    def save_current_image(self, name):
        image_arr = np.copy(self.data)
        for cluster in self.clusters:
            for p in cluster.pixels.keys():
                image_arr[p[0]][p[1]][0] = cluster.l
                image_arr[p[0]][p[1]][1] = cluster.a
                image_arr[p[0]][p[1]][2] = cluster.b
            image_arr[cluster.h][cluster.w][0] = 0
            image_arr[cluster.h][cluster.w][1] = 0
            image_arr[cluster.h][cluster.w][2] = 0

        self.save_lab_image(name, image_arr)

    def iterate_ntimes(self,n=1):
        """
        迭代n次，默认一次，并保存最终特征提取后的结果
        """
        self.init_clusters()
        self.move_clusters()
        for i in range(n):
            self.assignment()
            self.update_cluster()
        self.save_current_image('1.png')

    def get_color_difference(self,ord=2):
        '''
        计算每个聚类与其他聚类的色差范式结果，默认为均方差
        '''
        paradigm_lists=[]
        for i, cluster1 in enumerate(self.clusters):
            paradigm_list=[]
            color1 = LabColor(cluster1.l, cluster1.a, cluster1.b)
            for j, cluster2 in enumerate(self.clusters):
                if (i == j):
                    continue
                color2 = LabColor(cluster2.l, cluster2.a, cluster2.b)
                paradigm_list.append( delta_e_cie2000(color1, color2, Kl=1, Kc=1, Kh=1))
            paradigm_lists.append(np.linalg.norm(paradigm_list,ord=ord))
        return paradigm_lists

    def get_eachpixel_difference(self,ord=2):
        '''
        计算每个像素的色差范式结果，默认为均方差
        '''
        difference_list=[]
        for row in range(self.image_height):
            sub_list=[]
            for column in range(self.image_width):
                sub_list.append(0)
            difference_list.append(sub_list)

        sum_list=self.get_color_difference(ord)
        for i,cluster in enumerate(self.clusters):
            for p in cluster.pixels.keys():
                difference_list[p[0]][p[1]] =sum_list[i]

        return difference_list



def get_simliarity(p1_l,p2_l):
    """
    计算两图片相似度，色差的方差，值越小越相似
    """
    min = len(p1_l)
    if (min > len(p2_l)):
        min = len(p2_l)
    sum = 0
    for i in range(min):
        sum += math.pow((p1_l[i] - p2_l[i]), 2)
    return math.sqrt(sum)

if __name__ == '__main__':
    name1='13000.jpeg'
    p1 = SLICProcessor(name1, 64)
    p1.iterate_ntimes()
    p1_l = p1.get_color_difference()
    p1_l_eachpixel=p1.get_eachpixel_difference()
    print(p1_l)
    print(p1_l_eachpixel)
    print(len(p1_l_eachpixel))
    print(len(p1_l_eachpixel[0]))
    #p='Corel5k/13000/'
    #p1_sim=[]
    # for i in range(13000,13020):
    #     print(i)
    #     name2=p+str(i)+'.jpeg'
    #     p2 = SLICProcessor(name2, 64)
    #     p2.iterate_ntimes()
    #     p2_l = p2.get_color_difference()
    #
    #     p1_sim.append([get_simliarity(p1_l,p2_l),i])
    #
    # p1_sim.sort()
    # print(p1_sim)
