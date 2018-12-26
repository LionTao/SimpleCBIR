# CNN-CBIR
CBIR using keras and MobileNetV2

## Usage
```python
initCNNCache(dataset_path="/path/to/image/dataset") 

search(imagepath="/path/to/image/for/search", k=3)
```

## TODO
- [ ] Migrate from hdf5 to sqlite3
- [ ] API for using different models(such as VGG16, VGG19 and InceptionV3)