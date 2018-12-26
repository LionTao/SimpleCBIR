# CBIRDataset
Dataset module for [SimpleCBIR](https://github.com/LionTao/SimpleCBIR)

The Dataset in Powershell Script is [Corel 1k and Corel 10k Dataset](http://wang.ist.psu.edu/docs/related/)

Since the dataset mentioned above **does not contain labels**

I manually repack [Corel10K dataset](https://sites.google.com/site/dctresearch/Home/content-based-image-retrieval) in zip format and put it on my CDN bucket

Thanks to [Qiniu](https://www.qiniu.com/) for free CDN service

![QiniuLOGO](https://mars-assets.qnssl.com/qiniulogo/img-horizontal-blue-en.png)

## Run

Run python script `getDataset.py` will download labeled Corel10k Dataset to system temp folder from Qiniu CDN.    
Then the script will extract it to current directory using Python `zipfile` module. 
```bash
pip install requests # install dependency
python getDataset.py
```

### By the way
Run this command in Windows PowerShell will download [Corel 1k and Corel 10k Dataset](http://wang.ist.psu.edu/docs/related/) and extract it to current directory using [7zip](https://www.7-zip.org/)
```powershell
./getDataset.ps1
```

## TODO
- [ ] Add Stanford Dataset
- [ ] Using shell script instead