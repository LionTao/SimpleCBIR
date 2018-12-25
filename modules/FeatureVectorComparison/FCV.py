import cv2
import numpy as np
import modules.HistogramVector.hisvec as hv


def difference_between_image(img1: 'str', img2: 'str')->float:
    '''
    Compare two image.
    Firstly, get their feature vector.
    Then, calculate pair histograms' bhattacharyya distance.
    Finally, calculate the norm of the res vector.
    :param img1:
    :param img2:
    :return: a float number between 0(same) and 1(different)
    '''
    V1 = hv.get_vector(img1)
    V2 = hv.get_vector(img2)
    res = []
    for i in range(20):
        res.append(cv2.compareHist(V1[i], V2[i], cv2.HISTCMP_BHATTACHARYYA))
    return np.linalg.norm(res) / 20


def main():
    print(difference_between_image('130001.jpeg', '13000.jpeg'))


if __name__ == '__main__':
    main()
