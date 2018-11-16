from flask import Flask, request, jsonify

from model import load_graph, run_model, inference

from PIL import Image
import numpy as np
import cv2

graph = None

app = Flask(__name__)

@app.route('/', methods=['POST'])
def run_inference():
    img = request
    img = np.fromstring(img.get_data(), np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    cv2.imwrite("Image.jpg", img)
    seg_map = run_model(graph, img)
    action = inference(seg_map)

    return action

if __name__ == '__main__':

    graph = load_graph()
    app.run(port=8000)
