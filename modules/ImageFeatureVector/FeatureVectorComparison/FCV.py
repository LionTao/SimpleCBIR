import cv2
import numpy as np
import modules.ImageFeatureVector.HistogramVector.hisvec as hv


def difference_between_image(img1: str, img2: str) -> float:
    """
    Compare two image.
    Firstly, get their feature vector.
    Then, calculate pair histograms' bhattacharyya distance.
    Finally, calculate the norm of the res vector.
    :param img1:
    :param img2:
    :return: a float number between 0(same) and 1(different)
    """
    V1 = hv.get_vector(img1)
    V2 = hv.get_vector(img2)
    res = []
    for i in range(20):
        res.append(cv2.compareHist(V1[i], V2[i], cv2.HISTCMP_BHATTACHARYYA))
    return np.linalg.norm(res) / 20


def difference_between_image_vector(img: str, V: np.array) -> float:
    """
    Compare an image with a 20-histograms vector
    Firstly, get it feature vector.
    Then, calculate pair histograms' bhattacharyya distance.
    Finally, calculate the norm of the res vector.
    :param img:
    :param V: a 20-histograms array
    :return: a float number between 0(same) and 1(different)
    """
    _V = hv.get_vector(img)
    res = []
    for i in range(20):
        res.append(cv2.compareHist(_V[i], V[i], cv2.HISTCMP_BHATTACHARYYA))
    return np.linalg.norm(res) / 20


def main():
    print(difference_between_image('130001.jpeg', '13000.jpeg'))


if __name__ == '__main__':
    main()
