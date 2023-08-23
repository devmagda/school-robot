# Possible Screen Resolutions
# 320x180
# 960x540
import cv2

# Screen Settings
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540

# Color values in BGR color space
BGR_BLUE = [255, 0, 0]
BGR_PINK = [255, 0, 255]
BGR_RED = [0, 0, 255]
BGR_YELLOW = [0, 255, 255]
BGR_GREEN = [0, 255, 0]
BGR_TURQUOISE = [255, 255, 0]

# Color to filter
FILTER_COLOR = BGR_YELLOW

# HSV Detection Values
HSV_LIMIT_UPPER = 255
HSV_LIMIT_LOWER = 100
HSV_RANGE = 10

# K Means variables
KM_GROUP_COUNT = 2
KM_CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 5, 2.0)  # ( type, max_iter = 10 , epsilon = 1.0 )
KM_FLAGS = cv2.KMEANS_RANDOM_CENTERS
KM_TRIES = 100

