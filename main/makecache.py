def getDataset():
    import tempfile
    from modules.CBIRDataset.getDataset import GetDataSet
    temp_dir = tempfile.gettempdir() + '/SimpleCBIR_ResultTemp/'
    GetDataSet(des=temp_dir)
    print("DataSet should be ready at ", temp_dir + '/dataset')


def initCNNCBIR(dbpath):
    import tempfile
    from modules.CNNCBIR.search_api import initCNNCache
    temp_dir = tempfile.gettempdir() + '/SimpleCBIR_ResultTemp/'
    initCNNCache(dataset_path=temp_dir, dbpath=temp_dir)
    print("Database Cached at", dbpath + "index.sqlite")



if __name__ == '__main__':
    from modules.CNNCBIR.search_api import search
    import tempfile

    temp_dir = tempfile.gettempdir() + '/SimpleCBIR_ResultTemp/'
    initCNNCBIR(dbpath=temp_dir)
    res = search(
        imagepath="C:\\Users\\LionTao\\AppData\\Local\\Temp\\1\\SimpleCBIR_ResultTemp\\dataset\\art_1\\193000.jpg", k=3,
        dbpath="C:\\Users\\LionTao\\AppData\\Local\\Temp\\1\\SimpleCBIR_ResultTemp")
    print(res)
