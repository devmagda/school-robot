# Possible Screen Resolutions
# 320x180
# 960x540
# 800x600


import cv2

# import ImageUtils

# Screen Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# K Means variables
KM_GROUP_COUNT = 2
KM_CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 5, 2.0)  # ( type, max_iter = 10 , epsilon = 1.0 )
KM_FLAGS = cv2.KMEANS_RANDOM_CENTERS
KM_TRIES = 1

# Color values
# First parameter is color range for detecting hsv color space
# Second parameter is bgr color space
# Third parameter is rgb color space
COLOR_BLUE = (30, [255, 0, 0], [0, 0, 255])
COLOR_PINK = (10, [255, 0, 255], [255, 0, 255])
COLOR_RED = (20, [0, 0, 255], [255, 0, 0])  # Somehow doesn't work so good
COLOR_YELLOW = (10, [0, 255, 255], [255, 255, 0])
COLOR_GREEN = (20, [0, 255, 0], [0, 255, 0])
COLOR_TURQUOISE = (10, [255, 255, 0], [0, 255, 255])
COLOR_BLACK = (360, [0, 0, 0], [0, 0, 0])
COLOR_WHITE = (360, [255, 255, 255], [255, 255, 255])

COLOR_TRASH = COLOR_GREEN

# Color Pickers
# COLOR_PICKER_GREEN = ImageUtils.ColorPicker(COLOR_GREEN, KM_GROUP_COUNT)
# COLOR_PICKER_RED = ImageUtils.ColorPicker(COLOR_RED, KM_GROUP_COUNT)
# COLOR_PICKER_BLUE = ImageUtils.ColorPicker(COLOR_BLUE, KM_GROUP_COUNT)

# HSV Detection Values
HSV_LIMIT_UPPER = 255
HSV_LIMIT_LOWER = 75

# Shapes Text values
TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_FONT_SCALE = .5
TEXT_FONT_THICK = 1

# Human values
FILTER_FACES = True
EYES_MINIMUM = 2
FACES_COLOR = COLOR_GREEN
EYES_COLOR = COLOR_RED

# Scaling
FACE_COMPARISON_MARGIN = 50
FACE_COMPARISON_SCALE = 1 / 4
DO_FACE_COMPARISON = False
FACE_DETECTION_SCALE = 3 / 4

SCALE_OBJECT_DETECTION = 1.0  # NEVER change this value

# Info to print
INFO_FPS = False

SHOW_HELPER = False

# Image Detection Utils
MIRROR_HORIZONTAL = 1
MIRROR_VERTICAL = 0
MIRROR_BOTH = -1

MIRROR_VIEW = False

CLASSIFIER_FACE = 'haarcascade_frontalface_default.xml'
CLASSIFIER_EYE = 'haarcascade_eye.xml'


RECTANGLE_MAX_AGE = 3
