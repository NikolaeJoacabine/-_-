import sqlite3
from deepface import DeepFace
import cv2
import numpy
from dotenv import dotenv_values

config = dotenv_values(".env")
DATABASE_PATH = config["FACE_DATABASE_PATH"]


def get_vibe(face_img_path: str, name: str):
    face_img = cv2.imread(face_img_path)
    emotion = DeepFace.analyze(face_img, actions=["emotion"])
    return {name: emotion}

