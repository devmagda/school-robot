# Possible Screen Resolutions
# 320x180
# 960x540
import cv2

# Screen Settings
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540

# Color values in BGR color space
COLOR_BLUE = (10, [255, 0, 0], [0, 0, 255])
COLOR_PINK = (10, [255, 0, 255], [255, 0, 255])
COLOR_RED = (10, [0, 0, 255], [255, 0, 0])
COLOR_YELLOW = (10, [0, 255, 255], [255, 255, 0])
COLOR_GREEN = (20, [0, 255, 0], [0, 255, 0])
COLOR_TURQUOISE = (10, [255, 255, 0], [0, 255, 255])
COLOR_WHITE = (360, [0, 0, 0], [0, 0, 0])
COLOR_BLACK = (360, [255, 255, 255], [255, 255, 255])

# Color to filter
FILTER_COLOR = COLOR_GREEN

# HSV Detection Values
HSV_LIMIT_UPPER = 255
HSV_LIMIT_LOWER = 75
HSV_RANGE = 10

# K Means variables
KM_GROUP_COUNT = 2
KM_CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 5, 2.0)  # ( type, max_iter = 10 , epsilon = 1.0 )
KM_FLAGS = cv2.KMEANS_RANDOM_CENTERS
KM_TRIES = 100

# Shapes Text values
TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_FONT_SCALE = .5
TEXT_FONT_THICK = 1

