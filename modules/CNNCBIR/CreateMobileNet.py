def initMobileNet():
    from keras.applications.mobilenetv2 import MobileNetV2
    input_shape = (224, 224, 3)  # width and height should >= 48
    weight = 'imagenet'
    pooling = 'max'
    model = MobileNetV2(weights=weight, input_shape=(input_shape[0], input_shape[1], input_shape[2]), pooling=pooling,
                        include_top=False)
    return model


def extract_feat(model, img_path):
    from keras.preprocessing import image
    from keras.applications.vgg16 import preprocess_input
    import numpy.linalg as LA
    import numpy as np

    input_shape = (224, 224, 3)
    img = image.load_img(img_path, target_size=(input_shape[0], input_shape[1]))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    feat = model.predict(img)
    norm_feat = feat[0] / LA.norm(feat[0])
    return norm_feat
