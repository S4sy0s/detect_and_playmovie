import os
import cv2
import numpy as np

class FaceDetect:
    def __init__(self):
        ######################
        ##  face-detection-yunet-2023mar.onnxやyunet_n_dynamic.onnxは使えない
        ##  opencvのバージョンが異なるためかと考えられる.今使っているものは 「opencv == 4.6.0」
        #directory = os.path.dirname(__file__)
        #weights = os.path.join(directory, "model\\face-detection-yunet-2023mar.onnx")
        weights = "model\\face_detection_yunet_2022mar.onnx"
        self.face_detector = self._load_model(weights)

    def _load_model(self, weights):
        face_detector = cv2.FaceDetectorYN_create(weights, "", (0,0))
        return face_detector 

    def _draw_bbox(self, img, faces):
        for face in faces:
            box = list(map(int, face[:4]))
            color = (0, 0, 255)
            thickness = 2
            line = cv2.LINE_AA
            cv2.rectangle(img, box, color, thickness, line)

            landmarks = list(map(int, face[4:len(face)-1]))
            landmarks = np.array_split(landmarks, len(landmarks) / 2)
            
            radius = 5
            thickness = -1
            for landmark in landmarks:
                cv2.circle(img, landmark, radius, color, thickness, line)

            confidence = face[-1]
            confidence = "{:.2f}".format(confidence)
            position = (box[0], box[1] - 10)
            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 0.5
            thickness = 2
            cv2.putText(img, confidence, position, font, scale, color, thickness, line)
        
        return img

    def detect_draw(self, img):
        height, width, _ = img.shape
        self.face_detector.setInputSize((width, height))
        _, faces = self.face_detector.detect(img)
        #faces = faces if faces is not None else []
        if faces is None:
            output = img
        else:
            output = self._draw_bbox(img, faces)

        return output