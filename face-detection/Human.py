import Constants
import ImageUtils
from ImageUtils import ImageDetectionUtil
from Shapes import Rectangle

class Faces:

    @staticmethod
    def getValidFaces(gray, eyeCascade, faceCascade, scale=1.0):

        found = False

        # Scale image
        gray = ImageUtils.ImageDetectionUtil.scaleImage(gray, scale)

        faces = Faces.getFromImg(gray, faceCascade)

        c = 0

        validFaces = []

        if len(faces) == 0:
            # print("No faces found")
            return [], []

        for face in faces:
            roi, offset = ImageUtils.ImageDetectionUtil.getSubImage(gray, face.position)
            eyes = Eyes.getFromImg(roi, eyeCascade, offset=offset)
            x = len(eyes)
            if x >= Constants.EYES_MINIMUM or not Constants.FILTER_FACES:
                found = True
                face.scale(1/scale)
                validFaces.append(face)
                c = c + 1
                ImageUtils.ImageDetectionUtil.helperShow(roi, 'Faces')

        return validFaces, found

    @staticmethod
    def getFromImg(gray, cascade):
        return ImageDetectionUtil.getObjectByCascade(cascade, gray, color=Constants.FACES_COLOR)
    actions = ['age', 'gender', 'race', 'emotion']

    models = [
        'VGG-Face',
        'Facenet',
        'Facenet512',
        'OpenFace',
        'DeepFace',
        'DeepID',
        'ArcFace',
        'Dlib',
        'SFace',
    ]
    model_name = models[0]

    metrics = ['cosine', 'euclidean', 'euclidean_l2']
    distance_metric = metrics[0]

    backends = [
        'opencv',
        'ssd',
        'dlib',
        'mtcnn',
        'retinaface',
        'mediapipe',
        'yolov8',
        'yunet',
    ]
    detector_backend = backends[4]

    norms = [
        'base',
        'raw',
        'Facenet',
        'Facenet2018',
        'VGGFace',
        'VGGFace2',
        'ArcFace'
    ]
    normalization = norms[2]

    cached_face_data = None

    @staticmethod
    def initialize(face):
        Faces.cached_face_data = Faces.analyze(face, actions=['gender', 'race'])

    @staticmethod
    def represent(image):
        from deepface import DeepFace
        model = DeepFace.represent(
            image,
            model_name=Faces.model_name,
            detector_backend=Faces.detector_backend,
            normalization=Faces.normalization
        )
        return model

    @staticmethod
    def analyze(image, actions=['age', 'gender', 'race', 'emotion']) -> tuple[str, str, {}]:
        from deepface import DeepFace
        data = DeepFace.analyze(
            image,
            actions=actions,
            detector_backend=Faces.detector_backend,
            silent=True
        )
        return data[0]


    @staticmethod
    def get_race(image):
        data = Faces.analyze(image, actions=['race'])
        return data['dominant_race']

    @staticmethod
    def get_gender(image):
        data = Faces.analyze(image, actions=['gender'])
        return data['dominant_gender']

    @staticmethod
    def get_age(image):
        data = Faces.analyze(image, actions=['age'])
        return data['age']

    @staticmethod
    def get_emotion(image):
        data = Faces.analyze(image, actions=['emotion'])
        return data['dominant_emotion']

    @staticmethod
    def compare(face1, face2) -> tuple[int, float, float]:
        from deepface import DeepFace
        try:
            result = DeepFace.verify(
                img1_path=face1,
                img2_path=face2,
                model_name=Faces.model_name,
                distance_metric=Faces.distance_metric,
                detector_backend=Faces.detector_backend,
                enforce_detection=True,
                normalization=Faces.normalization)
            return int(result['verified']), result['distance'], result['threshold']
        except ValueError:
            return -1, 0.0, 0.0


class Eyes:

    @staticmethod
    def getFromImg(image, cascade, offset=[0, 0]):
        return ImageDetectionUtil.getObjectByCascade(cascade, image, offset, color=Constants.EYES_COLOR)
