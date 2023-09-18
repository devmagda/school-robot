import Constants
import ImageUtils
from ImageUtils import ImageDetectionUtil


class FacesUtil:

    # DeepFace Parameters

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

    # ----------------------------------------------------------------

    @staticmethod
    def get_valid_faces(gray, eyeCascade, faceCascade, scale=1.0):

        found = False

        # Scale image
        gray = ImageUtils.ImageDetectionUtil.scaleImage(gray, scale)

        faces = FacesUtil.getFromImg(gray, faceCascade)

        c = 0

        valid_faces = []

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
                valid_faces.append(face)
                c = c + 1
                ImageUtils.ImageDetectionUtil.helperShow(roi, 'Faces')

        return valid_faces, found

    @staticmethod
    def getFromImg(gray, cascade):
        return ImageDetectionUtil.getObjectByCascade(cascade, gray, color=Constants.FACES_COLOR)

    @staticmethod
    def initialize(face):
        FacesUtil.cached_face_data = FacesUtil.analyze(face, actions=['gender', 'race'])

    @staticmethod
    def represent(image):
        from deepface import DeepFace
        model = DeepFace.represent(
            image,
            model_name=FacesUtil.model_name,
            detector_backend=FacesUtil.detector_backend,
            normalization=FacesUtil.normalization
        )
        return model

    @staticmethod
    def analyze(image, actions=None) -> tuple[str, str, {}]:
        if actions is None:
            actions = ['age', 'gender', 'race', 'emotion']
        from deepface import DeepFace
        data = DeepFace.analyze(
            image,
            actions=actions,
            detector_backend=FacesUtil.detector_backend,
            silent=True
        )
        return data[0]

    @staticmethod
    def get_race(image):
        data = FacesUtil.analyze(image, actions=['race'])
        return data['dominant_race']

    @staticmethod
    def get_gender(image):
        data = FacesUtil.analyze(image, actions=['gender'])
        return data['dominant_gender']

    @staticmethod
    def get_age(image):
        data = FacesUtil.analyze(image, actions=['age'])
        return data['age']

    @staticmethod
    def get_emotion(image):
        data = FacesUtil.analyze(image, actions=['emotion'])
        return data['dominant_emotion']

    @staticmethod
    def compare(face1, face2) -> tuple[int, float, float]:
        from deepface import DeepFace
        try:
            result = DeepFace.verify(
                img1_path=face1,
                img2_path=face2,
                model_name=FacesUtil.model_name,
                distance_metric=FacesUtil.distance_metric,
                detector_backend=FacesUtil.detector_backend,
                enforce_detection=True,
                normalization=FacesUtil.normalization)
            return int(result['verified']), result['distance'], result['threshold']
        except ValueError:
            return -1, 0.0, 0.0


class Eyes:

    @staticmethod
    def getFromImg(image, cascade, offset=[0, 0]):
        return ImageDetectionUtil.getObjectByCascade(cascade, image, offset, color=Constants.EYES_COLOR)
