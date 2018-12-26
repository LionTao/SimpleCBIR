import cv2
import numpy
import modules.ColourDifference.slic as slic
# import modules.ImageFeatureExtract as ife
import modules.PatternDifference.ImProj as imp


def get_guass(shape: tuple) -> numpy.array:
    """
    :param shape: the shape of matrix
    :return: a matrix with 2D Gaussian distribution
    """
    x, y = numpy.meshgrid(numpy.linspace(-1, 1, shape[0]), numpy.linspace(-1, 1, shape[1]))
    d = numpy.sqrt(x * x + y * y)
    sigma, mu = 0.6, 0.0
    g = numpy.exp(-((d - mu) ** 2 / (2.0 * sigma ** 2)))
    return g.T


def get_his(img: numpy.array) -> float:
    """
    Firstly, get the image's histogram, then get the norm.
    :param img: image (split)
    :return: the norm the image's histogram
    """
    return cv2.calcHist([img], [0], None, [256], [0, 256])


def get_weight(file: str) -> numpy.array:
    """
    Using module ColourDifference and PatternDifference,
    to get the visually significant matrix
    :param file: the name of the file(due to the definition of others' interface)
    :return: the visually significant matrix
    """
    img = cv2.imread(file, 0)
    G = get_guass(img.shape)
    C_processor = slic.SLICProcessor(file, 64)
    C_processor.iterate_ntimes()
    C = C_processor.get_eachpixel_difference()
    P = imp.Pattern_Otherness_Calculation(file)
    D = numpy.multiply(C, P)
    diff_D = D.max() - D.min()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            D[i, j] = (D[i, j] - D.min()) / diff_D
    return numpy.multiply(D, G)


def get_vector(file: str) -> numpy.array:
    """
    Image retrieval based on spatial pyramid of visual saliency.
    :param file: image
    :return: feature vector V'
    """
    V = []
    img = cv2.imread(file, flags=0)
    length, width = img.shape
    l = 1
    a = [1]
    while l <= 2:
        a.append(a[l - 1] * 0.25)
        l += 1
    S = get_weight(file)
    l = 0
    while l <= 2:
        for i in range(2 * l):
            for j in range(2 * l):
                W = numpy.sum(S[i * width:(i + 1) * width, j * length:(j + 1) * length])
                split_img = img[i * width:(i + 1) * width, j * length:(j + 1) * length]
                V.append(get_his(split_img) * W * a[l])
        length, width = length // 2, width // 2
        l += 1
    return V


def main():
    print(get_vector('13000.jpeg'))


if __name__ == '__main__':
    main()
