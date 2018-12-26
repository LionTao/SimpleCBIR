def DownloadFile(file_url, file_path):
    import requests
    from contextlib import closing
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    with closing(requests.get(file_url, headers=headers, stream=True)) as response:
        chunk_size = 1024  # 单次请求最大值
        content_size = int(response.headers['content-length'])  # 内容体总大小
        data_count = 0
        with open(file_path, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                data_count = data_count + len(data)
                now_jd = (data_count / content_size) * 100
                print("\r Progress: {:.2f}% ({:d}/{:d}) - {}".format(now_jd, data_count, content_size, file_path),
                      end=" ")
        print("\nDownload Completed.")


def ExtractZip(path, des=""):
    import os
    import zipfile
    print("Checking Dataset directory...")
    if not os.path.exists("dataset"):
        print("Directory not found.")
        os.mkdir("dataset")
        print("Directory successfully created.")

    print("\nStart unzip....This may take a while...")
    file_zip = zipfile.ZipFile(path, 'r')
    for file in file_zip.namelist():
        file_zip.extract(file, des + 'dataset/')
        print("\r Progress: {:.2f}%".format((file_zip.namelist().index(file) / len(file_zip.namelist())) * 100), end='')
    print("\r Progress: 100.00%")
    file_zip.close()


def GetDataSet():
    import tempfile
    cdn_url = "http://media.liontao.xin/CorelDB.zip?token=8D-fPY7fZfvNQ_YlcCHphmf-beQ7s5-ahx1C_WJ4:B4fco3kqXcyC3Ast57tWaAxHCj4"

    _, file_path = tempfile.mkstemp(suffix=".zip", prefix="SimpleCBIR_")
    DownloadFile(cdn_url, file_path)
    ExtractZip(file_path)
    print("Dataset is ready.")


if __name__ == '__main__':
    GetDataSet()
