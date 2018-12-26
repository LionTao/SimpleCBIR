def Pattern_Otherness_Calculation(ImageDirectory):
    import cv2
    import numpy as np

    srcimg = cv2.imread(ImageDirectory,0)
    srcheight,srcwidth=srcimg.shape
    height,width = srcimg.shape

#    print(srcimg)

#   将图像resize至边长为9的倍数
    if height % 9 != 0:
        height = height + (9 - height % 9)
    if width % 9 != 0:
        width = width + (9 - width % 9)
    dstimg = cv2.resize(srcimg,dsize=(width,height),interpolation=cv2.INTER_CUBIC)
#    print(dstimg.shape)

    N = height * width // 81          #划分后的图像块个数
    ImageList = []                    #存储图像矩阵
    OthernessList = []                #存储差异性矩阵
    Normalization = []                #存储归一化后的结果
    sum = np.mat(np.zeros((9,9)))

    for i in range(height // 9):
        for j in range(width // 9):
            sum+=dstimg[i * 9:(i + 1) * 9,j * 9:(j + 1) * 9]
            ImageList.append(dstimg[i * 9:(i + 1) * 9,j * 9:(j + 1) * 9])
    Pa = sum / N                        #平均图像块
    for i in range(N):
        OthernessList.append(np.sum(np.abs(Pa - ImageList[i])))

#   归一化
    maxOtherness = max(OthernessList)
    minOtherness = min(OthernessList)
    for i in range(N):
        Normalization.append((OthernessList[i] - minOtherness) / (maxOtherness - minOtherness))
#    print(Normalization)


#   将归一化结果中每一个元素扩充为dstimg尺寸的矩阵，即每个元素复制为9x9的图像块大小
    temp_res=np.repeat(np.repeat(np.resize(Normalization,(height//9,width//9)),9,axis=0),9,axis=1)
#    print(temp_res)

#   将归一化结果扩充为dstimg尺寸的矩阵后，将其还原为原始图像尺寸,得到最终结果
    orig_res = cv2.resize(temp_res,dsize=(srcwidth,srcheight),interpolation=cv2.INTER_CUBIC)
#    print(orig_res)

    return orig_res
