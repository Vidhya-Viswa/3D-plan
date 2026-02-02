import os
import sys
import json
from io import BytesIO
from datetime import datetime

import tensorflow as tf
tf.compat.v1.disable_eager_execution()

from keras import backend as K


import PIL
from PIL import Image
import numpy
from numpy import zeros, asarray, expand_dims
import numpy as np




from skimage import color


from matplotlib import pyplot
from matplotlib.patches import Rectangle

from keras.backend import clear_session

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS




from mrcnn.config import Config
from mrcnn.model import MaskRCNN, mold_image
from mrcnn.utils import extract_bboxes


tf.compat.v1.disable_eager_execution()

global _model
global _graph
global cfg

_graph = tf.compat.v1.Graph()
_sess = tf.compat.v1.Session(graph=_graph)

with _graph.as_default():
    K.set_session(_sess)
ROOT_DIR = os.path.abspath("./")
WEIGHTS_FOLDER = "./weights"

sys.path.append(ROOT_DIR)

MODEL_NAME = "mask_rcnn_hq"
WEIGHTS_FILE_NAME = 'maskrcnn_15_epochs.h5'

application=Flask(__name__)
cors = CORS(application, resources={r"/*": {"origins": "*"}})


class PredictionConfig(Config):
	# define the name of the configuration
	NAME = "floorPlan_cfg"
	# number of classes (background + door + wall + window)
	NUM_CLASSES = 1 + 3
	# simplify GPU config
	GPU_COUNT = 1
	IMAGES_PER_GPU = 1
	
@application.before_first_request
def load_model():
    global _model, cfg

    with _graph.as_default():
        K.set_session(_sess)

        model_folder_path = os.path.abspath("./") + "/mrcnn"
        weights_path = os.path.join(WEIGHTS_FOLDER, WEIGHTS_FILE_NAME)

        cfg = PredictionConfig()

        print("Loading Mask R-CNN model...")
        _model = MaskRCNN(
            mode="inference",
            model_dir=model_folder_path,
            config=cfg
        )

        _model.load_weights(weights_path, by_name=True)
        print("Model loaded successfully")

	



def myImageLoader(imageInput):
    image = np.asarray(imageInput)

    # grayscale → RGB
    if image.ndim == 2:
        image = color.gray2rgb(image)

    # RGBA → RGB
    if image.shape[-1] == 4:
        image = image[..., :3]

    h, w, c = image.shape
    return image, w, h



def getClassNames(classIds):
	result=list()
	for classid in classIds:
		data={}
		if classid==1:
			data['name']='wall'
		if classid==2:
			data['name']='window'
		if classid==3:
			data['name']='door'
		result.append(data)	

	return result				

def normalizePoints(bbx, class_ids):
    result = []
    doorHeights = []

    # First pass – collect door sizes
    for i, bb in enumerate(bbx):
        if class_ids[i] == 3:  # door
            height = abs(bb[2] - bb[0])
            doorHeights.append(height)

    avgDoor = np.mean(doorHeights) if doorHeights else 0

    # Second pass – correct classes
    corrected_classes = []

    for i, bb in enumerate(bbx):
        class_id = class_ids[i]
        height = abs(bb[2] - bb[0])

        # window → door
        if class_id == 2 and avgDoor > 0 and height > avgDoor * 0.9:
            class_id = 3

        # door → window
        if class_id == 3 and avgDoor > 0 and height < avgDoor * 0.75:
            class_id = 2

        corrected_classes.append(class_id)
        result.append([bb[0], bb[1], bb[2], bb[3]])

    return result, avgDoor, corrected_classes

		

def turnSubArraysToJson(objectsArr):
	result=list()
	for obj in objectsArr:
		data={}
		data['x1']=obj[1]
		data['y1']=obj[0]
		data['x2']=obj[3]
		data['y2']=obj[2]
		result.append(data)
	return result



@application.route('/', methods=['POST'])
def prediction():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        imagefile = Image.open(file.stream)
        image, w, h = myImageLoader(imagefile)

        scaled_image = mold_image(image, cfg)
        sample = expand_dims(scaled_image, 0)

        with _graph.as_default():
            r = _model.detect(sample, verbose=0)[0]

        bbx = r['rois'].tolist()
        points, averageDoor, fixed_classes = normalizePoints(bbx, r['class_ids'])

        return jsonify({
    "points": turnSubArraysToJson(points),
    "classes": getClassNames(fixed_classes),
    "Width": w,
    "Height": h,
    "averageDoor": averageDoor,
    "wallThickness": averageDoor * 0.15

        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

@application.route('/ping', methods=['GET'])
def ping():
    return {"status": "server is running"}


		
    
if __name__ =='__main__':
	application.debug=True
	print('===========before running==========')
	application.run()
	print('===========after running==========')
