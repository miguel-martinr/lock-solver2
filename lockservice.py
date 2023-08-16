import cv2
from computervision import get_text_from_image_at_rectangle, imshow


def get_switches_rectangles():
    switches_rectangles = [
        [
            [
                (1070, 195),
                (1130, 213)
            ],
        ],
        [
            [
                (1070, 273),
                (1130, 290)
            ],
        ],
        [
            [
                (1070, 350),
                (1130, 370)
            ],
        ],
        [
            [
                (1070, 428),
                (1130, 445)
            ],
        ],
        [
            [
                (1070, 505),
                (1130, 522)
            ],
        ],
        [
            [
                (1070, 581),
                (1130, 600)
            ],
        ],
        [
            [
                (1070, 660),
                (1130, 678)
            ],
        ],
        [
            [
                (1070, 736),
                (1130, 754),
            ]
        ],
    ]

    for rect in switches_rectangles:
        r = rect[0]
        top_left = (r[0][0] + 97, r[0][1])
        button_right = (r[1][0] + 97, r[1][1])
        rect.append((top_left, button_right))


    return switches_rectangles

def get_input_voltage_rectangle():
    input_voltage_rectangle = [
        (498, 498),
        (555, 530)
    ]

    return input_voltage_rectangle


def get_expected_voltage_rectangles():
    rectangles = [
        [
            (1369, 495),
            (1423, 531)
        ],
        [
            (1369, 550),
            (1423, 586)
        ]
    ]

    return rectangles


def get_input_voltage_from_image(image):
    input_voltage_rectangle = get_input_voltage_rectangle()

    input_voltage_text = get_text_from_image_at_rectangle(image, input_voltage_rectangle)

    return input_voltage_text

def get_switches_data_from_image(image):
    
    switches_rectangles = get_switches_rectangles()            
    switches_data = []
    for red, blue in switches_rectangles:
        sym_rectangle_red = [
            red[0],
            (red[0][0] + 26, red[1][1])
        ]

        num_rectangle_red = [
            (red[0][0] + 26, red[0][1]),
            red[1]
        ]

        # # Show the sym rectangle
        # imshow(image[
        #     sym_rectangle_red[0][1]:sym_rectangle_red[1][1],
        #     sym_rectangle_red[0][0]:sym_rectangle_red[1][0]
        # ])        

        # # Show the num rectangle
        # imshow(image[
        #     num_rectangle_red[0][1]:num_rectangle_red[1][1],
        #     num_rectangle_red[0][0]:num_rectangle_red[1][0]
        # ])


        red_sym_data = get_text_from_image_at_rectangle(image, sym_rectangle_red, whitelist='+-*/')
        red_num_data = get_text_from_image_at_rectangle(image, num_rectangle_red, whitelist='0123456789')
        red_data = red_sym_data + red_num_data
        
        sym_rectangle_blue = [
            blue[0],
            (blue[0][0] + 26, blue[1][1])
        ]

        num_rectangle_blue = [
            (blue[0][0] + 26, blue[0][1]),
            blue[1]
        ]

        blue_sym_data = get_text_from_image_at_rectangle(image, sym_rectangle_blue, whitelist='+-*/')
        blue_num_data = get_text_from_image_at_rectangle(image, num_rectangle_blue, whitelist='0123456789')
        blue_data = blue_sym_data + blue_num_data

        switches_data.append([red_data, blue_data])

    return switches_data

def get_expected_voltages_from_image(image):    
    expected_voltages_rectangles = get_expected_voltage_rectangles()
    expected_voltages_data = []
    for rect in expected_voltages_rectangles:
        expected_voltages_data.append(get_text_from_image_at_rectangle(image, rect))

    return expected_voltages_data


image = cv2.imread('images/13477898-6d31-493c-8c8f-942f2ffc0f7e.jpeg')


