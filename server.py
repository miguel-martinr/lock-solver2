from base64 import b64encode
import cv2
from locksolver.lockservice import get_expected_voltage_rectangles, get_input_voltage_rectangle, get_switches_data_from_image, get_expected_voltages_from_image, get_input_voltage_from_image, get_switches_rectangles
from locksolver.switches import solve_lock
from flask import Flask, request, jsonify
import numpy as np
# CORS
from flask_cors import CORS
import awsgi

def parse_image(image):
    switches = get_switches_data_from_image(image)
    expected_voltages = get_expected_voltages_from_image(image)
    input_voltage = get_input_voltage_from_image(image)

    switches_images_rects = get_switches_rectangles()
    switches_images = []
    for red, blue in switches_images_rects:
        switches_images.append(image[red[0][1]:red[1][1], red[0][0]:red[1][0]])
        switches_images.append(image[blue[0][1]:blue[1][1], blue[0][0]:blue[1][0]])

    expected_voltages_rects = get_expected_voltage_rectangles()
    expected_voltages_images = []
    for rect in expected_voltages_rects:
        expected_voltages_images.append(image[rect[0][1]:rect[1][1], rect[0][0]:rect[1][0]])

    input_voltage_rect = get_input_voltage_rectangle()
    input_voltage_image = image[input_voltage_rect[0][1]:input_voltage_rect[1][1], input_voltage_rect[0][0]:input_voltage_rect[1][0]]
                    
    return input_voltage, expected_voltages, switches, input_voltage_image, expected_voltages_images, switches_images


def solve_image(image):
    
    input_voltage, expected_voltages, switches = parse_image(image)
    return solve_lock(input_voltage, expected_voltages, switches)



app = Flask(__name__)


# CORS
CORS(app)

def encode_image(image):
    _, buffer = cv2.imencode('.jpg', image)
    result = b64encode(buffer).decode('utf-8')
    return result


@app.route('/image-params', methods=['POST'])
def image():
        
    image = request.files['image'].read()
    image = cv2.imdecode(np.frombuffer(image, np.uint8), -1)

    input_voltage, expected_voltages, switches, input_voltage_image, expected_voltages_images, switches_images = parse_image(image)

    

    return jsonify({
        'input_voltage': input_voltage,
        'expected_voltages': expected_voltages,
        'switches': switches,
        'input_voltage_image': encode_image(input_voltage_image),
        'expected_voltages_images': [encode_image(image) for image in expected_voltages_images],
        'switches_images': [encode_image(image) for image in switches_images]        
    })

# Ruta por defecto
@app.route('/', methods=['GET'])
def index():
    return 'Welcome to Lock Solver API'


def handler(event, context):
    return awsgi.response(app, event, context)
    

