def get_imlist(path, res: list) -> None:
    """
    search for jpeg recursively in the given folder
    :param path: path to images
    :param res: res list for recursive search
    :return: None
    """
    import os

    for e in os.listdir(path):
        filepath = os.path.join(path, e)
        if os.path.isfile(filepath):
            if os.path.basename(filepath).endswith('.jpg') or \
                    os.path.basename(filepath).endswith('.jpeg'):
                res.append(filepath)
        elif os.path.isdir(filepath):
            get_imlist(filepath, res)


def search(imagepath: str, k: int, dbname="index.sqlite") -> list:
    """
    API for CNN search
    :param imagepath: The image for search
    :param k: num of images to return
    :return:list of paths of images
    """


    import numpy as np
    import h5py  # db
    import sqlite3
    import os

    # import matplotlib.pyplot as plt
    # import matplotlib.image as mpimg
    from modules.CNNCBIR.CreateMobileNet import extract_feat
    from modules.CNNCBIR.CreateMobileNet import initMobileNet

    if not os.path.exists(dbname):
        raise Exception("Data Cache not initialized")
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    db = h5py.File("index.h5", 'r')
    feats = db['dataset_1'][:]
    imgNames = db['dataset_2'][:]
    db.close()

    print("searching starts")

    # read and show query image
    queryDir = imagepath
    # queryImg = mpimg.imread(queryDir)
    # plt.title("Query Image")
    # plt.imshow(queryImg)
    # plt.show()

    # Create MobileNetV2 model
    model = initMobileNet()

    # extract query image's feature, compute simlarity score and sort
    queryVec = extract_feat(model, queryDir)
    scores = np.dot(queryVec, feats.T)
    rank_ID = np.argsort(scores)[::-1]
    rank_score = scores[rank_ID]

    # number of top retrieved images to show
    maxres = k
    res = [imgNames[index] for i, index in enumerate(rank_ID[0:maxres])]
    print("top %d images in order are: " % maxres, res)

    # for i, im in enumerate(res):
    #     image = mpimg.imread(str(im, 'utf-8'))
    #     plt.title("search output %d" % (i + 1))
    #     plt.imshow(image)
    #     plt.show()

    return res


def initCNNCache(dataset_path="dataset", dbname="index.sqlite") -> None:
    """
    make cache for image features
    :param dataset_path: path to image dataset
    :param dbname: name of sqliteDB(TODO)
    :return: None
    """

    import numpy as np
    import h5py
    import os
    import sqlite3
    from modules.CNNCBIR.CreateMobileNet import initMobileNet, extract_feat

    if os.path.exists(dbname):
        os.remove(dbname)
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE CNN_CACHE
           (
           NAME           TEXT    NOT NULL,
           FEATURE        blob   NOT NULL 
           );''')
    conn.commit()
    sql = "INSERT INTO CNN_CACHE (NAME,FEATURE) VALUES(?,?)"
    img_list = list()
    get_imlist(dataset_path, img_list)
    # print(img_list);exit(0)

    print("Start Caching Features")

    feats = []
    names = []

    model = initMobileNet()
    for i, img_path in enumerate(img_list):
        norm_feat = extract_feat(model=model, img_path=img_path)
        norm_feat.tostring(order='C')
        # img_name = os.path.split(img_path)[1]
        feats.append(norm_feat)
        # names.append(img_name)
        names.append(img_path)
        cursor.execute(sql, (img_path, norm_feat.tobytes()))
        print("\rextracting feature from image No. {} , {} images in total".format((i + 1), len(img_list)), end='')
    conn.commit()
    conn.close()
    feats = np.array(feats)
    # print(feats)
    # directory for storing extracted features
    output = "index.h5"

    print("\nDumping cache result to ", output)

    h5f = h5py.File(output, 'w')
    h5f.create_dataset('dataset_1', data=feats)
    # h5f.create_dataset('dataset_2', data = names)
    h5f.create_dataset('dataset_2', data=np.string_(names))
    h5f.close()


if __name__ == '__main__':
    initCNNCache(dataset_path="C:\\Users\\LionTao\\Documents\\Projects\\CBIRDataset\\dataset")
    search("target.jpg", 3)
