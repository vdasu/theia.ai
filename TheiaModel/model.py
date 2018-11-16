import os

import tensorflow as tf
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import gridspec
import cv2

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

FROZEN_GRAPH = "frozen_inference_graph.pb"
INPUT_TENSOR = 'ImageTensor:0'
OUTPUT_TENSOR = 'SemanticPredictions:0'
HEIGHT = 384
WIDTH = 384

LABEL_NAMES = np.asarray([
    'road', 'sidewalk', 'building', 'wall', 'fence', 'pole', 'traffic_light',
    'traffic_sign', 'vegetation', 'terrain', 'sky', 'person', 'rider', 'car', 'truck',
    'bus', 'train', 'motorcycle', 'bicyle'
])

MINIMUM_WALK_RATIO = 0.2
MINIMUM_POLE_RATIO = 0.05
MINIMUM_VEHICLE_RATIO = 0.2
MINIMUM_BIKE_RATIO = 0.1

def load_graph():

    graph = tf.Graph()
    graph_def = tf.GraphDef()

    with tf.gfile.GFile(FROZEN_GRAPH, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def, name='')

    return graph

def run_model(graph, img):

    img = cv2.resize(img, (HEIGHT, WIDTH), interpolation = cv2.INTER_AREA)
    
    seg_map = None
    with tf.Session(graph=graph) as sess:
        seg_map = sess.run(OUTPUT_TENSOR, feed_dict={INPUT_TENSOR: [np.asarray(img)]})[0]
    
    return seg_map

def inference(seg_map):

    left_score = 0
    right_score = 0
    centre_score = 0
    vehicle_score = 0
    bike_score = 0
    obstacle_score = 0

    for i in range(HEIGHT):
        for j in range(WIDTH):
            left = j <= WIDTH/2
            right = j > WIDTH/2
            centre = (j >= WIDTH/3 and j <= (WIDTH / 3)*2)

            label = LABEL_NAMES[seg_map[i][j]]

            if (label == 'terrain' or label == 'sidewalk'):
                if (centre):
                    centre_score += 1
                if (left):
                    left_score += 1
                else:
                    right_score += 1
            elif label == 'pole':
                obstacle_score += 1
            elif (label == 'car' or label == 'truck'):
                vehicle_score += 1
            elif (label == 'bicyle' or label == 'motorcycle'):
                bike_score += 1
                
    if (left_score > right_score):
        left_walk_ratio = left_score / ((HEIGHT*WIDTH) / 2.0)
        if (left_walk_ratio < MINIMUM_WALK_RATIO):
            left_score = 0
    else:
        right_walk_ratio = right_score / ((HEIGHT*WIDTH) / 2.0)
        if (right_walk_ratio < MINIMUM_WALK_RATIO):
            right_score = 0
    
    centre_walk_ratio = centre_score / ((HEIGHT*WIDTH) / 2.0)
    if (centre_walk_ratio < MINIMUM_WALK_RATIO):
        centre_score = 0
    
    obstacle_ratio = obstacle_score / ((HEIGHT*WIDTH))
    if (obstacle_ratio < MINIMUM_POLE_RATIO):
        obstacle_score = 0
    
    vehicle_ratio = vehicle_score / ((HEIGHT*WIDTH))
    if (vehicle_ratio < MINIMUM_VEHICLE_RATIO):
        vehicle_score = 0
    
    bike_ratio = bike_score / ((HEIGHT*WIDTH))
    if (bike_ratio < MINIMUM_BIKE_RATIO):
        bike_score = 0
    
    walk_position = ""
    is_vehicle = False
    is_obstacle = False
    is_bike = False

    if (centre_score > 0):
        walk_position = "front"
    elif (left_score > 0 and right_score > 0):
        if (left_score > right_score):
            walk_position = "left"
        else:
            walk_position = "right"
    else:
        walk_position = "none"
    
    if (obstacle_score > 0):
        is_obstacle = True
    
    if (vehicle_score > 0):
        is_vehicle = True
    
    if (bike_score > 0):
        is_bike = True

    action = ""
    if (walk_position == "none"):
        action += "Do not walk. Stay where you are."
    elif (walk_position == "front"):
        action += "Walk in front."
    elif (walk_position == "left"):
        action += "Walk to your left."
    elif (walk_position == "right"):
        action += "Walk to your right."
    
    if (is_obstacle):
        action += " There are some obstacles ahead, careful."
    if (is_vehicle):
        action += " There are some vehicles ahead, careful."
    if (is_bike):
        action += " There are some bikes ahead, careful."

    return action
