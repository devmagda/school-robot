# Possible Screen Resolutions
# 320x180
# 960x540
import cv2

# import ImageUtils

# Screen Settings
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540

# K Means variables
KM_GROUP_COUNT = 2
KM_CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 5, 2.0)  # ( type, max_iter = 10 , epsilon = 1.0 )
KM_FLAGS = cv2.KMEANS_RANDOM_CENTERS
KM_TRIES = 10

# Color values
# First parameter is color range for detecting hsv color space
# Second parameter is bgr color space
# Third parameter is rgb color space
COLOR_BLUE = (10, [0, 0, 255], [255, 0, 0])
COLOR_PINK = (10, [255, 0, 255], [255, 0, 255])
COLOR_RED = (10, [255, 0, 0], [0, 0, 255])
COLOR_YELLOW = (10, [0, 255, 255], [255, 255, 0])
COLOR_GREEN = (20, [0, 255, 0], [0, 255, 0])
COLOR_TURQUOISE = (10, [255, 255, 0], [0, 255, 255])
COLOR_WHITE = (360, [0, 0, 0], [0, 0, 0])
COLOR_BLACK = (360, [255, 255, 255], [255, 255, 255])

# Color Pickers
# COLOR_PICKER_GREEN = ImageUtils.ColorPicker(COLOR_GREEN, KM_GROUP_COUNT)
# COLOR_PICKER_RED = ImageUtils.ColorPicker(COLOR_RED, KM_GROUP_COUNT)
# COLOR_PICKER_BLUE = ImageUtils.ColorPicker(COLOR_BLUE, KM_GROUP_COUNT)

# HSV Detection Values
HSV_LIMIT_UPPER = 255
HSV_LIMIT_LOWER = 75
HSV_RANGE = 10

# Shapes Text values
TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_FONT_SCALE = .5
TEXT_FONT_THICK = 1

# Human values
FILTER_FACES = True
FACES_COLOR = COLOR_GREEN
EYES_COLOR = COLOR_RED

# Scaling
SCALE_FACE_DETECTION = 0.5
SCALE_OBJECT_DETECTION = 1.0  # NEVER change this value

# Info to print
INFO_FPS = True