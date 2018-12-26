from imageai.Detection import ObjectDetection
import os
import numpy as np

execution_path = os.getcwd()

detector = ObjectDetection()

detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel(detection_speed="flash")
detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path, "timg.jpg"),
                                             output_image_path=os.path.join(execution_path, "imagenew.jpg"))

for eachObject in detections:
    print(eachObject["name"] + " : " + str(eachObject["percentage_probability"]))
    print("--------------------------------")
