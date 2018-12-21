import numpy as np


def do_retrival(image, spx):
    """
    Image retrival based on spatial pyramid of visual saliency
    :param spx: S(p(x))
    :param image: example image Q in the color database K
    :return: feature vector V
    """
    v = np.empty(image.shape)

    # TODO:divide the image Q into blocks with level1 and level2

    l = 0

    while l <= 2:
        alpha_l = 0.5 ** (2 * l)
        l = l + 1

    # TODO:calculate S(p(x)) for image Q

    l = 0

    while l <= 2:
        for i in (1, 2 * l + 1):
            W_i_l = np.sum(spx)

    return v
