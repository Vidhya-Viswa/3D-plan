import os
import PIL
import numpy as np
from numpy import expand_dims
from mrcnn.config import Config
from mrcnn.model import MaskRCNN, mold_image
from skimage import color
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import tensorflow as tf
import sys

tf.compat.v1.disable_eager_execution()

global _model
global _graph
global cfg
global _sess

ROOT_DIR = os.path.abspath("./")
WEIGHTS_FOLDER = "./weights"
WEIGHTS_FILE_NAME = 'maskrcnn_15_epochs.h5'

application = Flask(__name__)
cors = CORS(application, resources={r"/*": {"origins": "*"}})

CONFIDENCE_THRESHOLD = 0.5

class PredictionConfig(Config):
    NAME = "floorPlan_cfg"
    NUM_CLASSES = 1 + 3
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

@application.before_first_request
def load_model():
    global cfg, _model, _graph, _sess
    try:
        _graph = tf.compat.v1.Graph()
        _sess = tf.compat.v1.Session(graph=_graph)
        with _graph.as_default():
            tf.compat.v1.keras.backend.set_session(_sess)
            model_folder_path = os.path.join(ROOT_DIR, "mrcnn")
            weights_path = os.path.join(WEIGHTS_FOLDER, WEIGHTS_FILE_NAME)
            if not os.path.exists(weights_path):
                raise FileNotFoundError(f"Weights file not found: {weights_path}")
            cfg = PredictionConfig()
            print("Loading Mask R-CNN model...")
            _model = MaskRCNN(mode='inference', model_dir=model_folder_path, config=cfg)
            _model.load_weights(weights_path, by_name=True)
            print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)

def myImageLoader(imageInput):
    try:
        image = np.asarray(imageInput)
        if image.ndim == 2:
            image = color.gray2rgb(image)
        elif image.shape[-1] == 4:
            image = image[..., :3]
        if image.ndim != 3:
            raise ValueError("Unsupported image dimensions")
        h, w, c = image.shape
        max_dim = 1024
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            new_w, new_h = int(w * scale), int(h * scale)
            image = PIL.Image.fromarray(image).resize((new_w, new_h), PIL.Image.ANTIALIAS)
            image = np.asarray(image)
            w, h = new_w, new_h
        return image, w, h
    except Exception as e:
        raise ValueError(f"Error processing image: {e}")

def getClassNames(classIds):
    result = []
    for classid in classIds:
        if classid == 1:
            result.append({"name": "wall"})
        elif classid == 2:
            result.append({"name": "window"})
        elif classid == 3:
            result.append({"name": "door"})
    return result

def filterAll(bbx, class_ids, scores):
    filtered_bbx = []
    filtered_classes = []
    for i, class_id in enumerate(class_ids):
        if scores[i] >= CONFIDENCE_THRESHOLD:  # Include all with high confidence
            filtered_bbx.append(bbx[i])
            filtered_classes.append(class_id)
    return filtered_bbx, filtered_classes

def turnSubArraysToJson(objectsArr):
    result = []
    for obj in objectsArr:
        data = {
            'x1': obj[1],
            'y1': obj[0],
            'x2': obj[3],
            'y2': obj[2]
        }
        result.append(data)
    return result

@application.route('/', methods=['POST'])
def prediction():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    file = request.files['image']
    if file.filename == '' or not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({"error": "Invalid or empty filename. Only PNG/JPG allowed."}), 400
    try:
        imagefile = PIL.Image.open(file.stream)
        image, w, h = myImageLoader(imagefile)
        print(f"Processed image dimensions: {h} x {w}")
        scaled_image = mold_image(image, cfg)
        sample = expand_dims(scaled_image, 0)
        with _graph.as_default():
            tf.compat.v1.keras.backend.set_session(_sess)
            r = _model.detect(sample, verbose=0)[0]
        
        bbx = r['rois'].tolist()
        class_ids = r['class_ids']
        scores = r['scores']
        
        points, fixed_classes = filterAll(bbx, class_ids, scores)
        
        wall_count = fixed_classes.count(1)
        window_count = fixed_classes.count(2)
        door_count = fixed_classes.count(3)
        
        return jsonify({
            "points": turnSubArraysToJson(points),
            "classes": getClassNames(fixed_classes),
            "Width": w,
            "Height": h,
            "counts": {"walls": wall_count, "windows": window_count, "doors": door_count}
        })
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 500

@application.route('/ping', methods=['GET'])
def ping():
    return {"status": "server is running"}

if __name__ == '__main__':
    print('===========Starting server==========')
    application.run(debug=False)
    print('===========Server stopped==========')

