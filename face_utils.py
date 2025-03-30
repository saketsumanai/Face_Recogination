import cv2
import numpy as np
import base64
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)

class FaceProcessor:
    def __init__(self):
        try:
            # Log available Haar cascade files
            cascade_dir = cv2.data.haarcascades
            logger.debug(f"Haar cascades directory: {cascade_dir}")
            available_files = os.listdir(cascade_dir)
            logger.debug(f"Available cascade files: {available_files}")

            cascade_path = os.path.join(cascade_dir, 'haarcascade_frontalface_default.xml')
            logger.debug(f"Loading cascade file from: {cascade_path}")

            if not os.path.exists(cascade_path):
                raise FileNotFoundError(f"Cascade file not found at {cascade_path}")

            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            if self.face_cascade.empty():
                raise ValueError("Failed to load cascade classifier")

            logger.info("Successfully initialized face cascade classifier")
            self.known_faces = []
            self.known_names = []

        except Exception as e:
            logger.error(f"Error initializing FaceProcessor: {str(e)}")
            raise

    def _process_base64_image(self, base64_image):
        """Convert base64 image to numpy array"""
        try:
            encoded_data = base64_image.split(',')[1]
            nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
            return cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise

    def _get_face_roi(self, image):
        """Extract face region from image"""
        faces = self.face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
        if len(faces) == 0:
            return None
        if len(faces) > 1:
            return None

        x, y, w, h = faces[0]
        face_roi = image[y:y+h, x:x+w]
        return cv2.resize(face_roi, (100, 100))  # Normalize size

    def _compare_faces(self, face1, face2):
        """Compare two face images using structural similarity"""
        try:
            # Ensure both images have the same size
            face1 = cv2.resize(face1, (100, 100))
            face2 = cv2.resize(face2, (100, 100))

            # Calculate mean squared error between the images
            error = np.sum((face1.astype("float") - face2.astype("float")) ** 2)
            error = error / float(face1.shape[0] * face1.shape[1])

            # Lower error means more similar faces
            similarity_threshold = 2000  # Adjust this threshold based on testing
            return error < similarity_threshold, error
        except Exception as e:
            logger.error(f"Error comparing faces: {str(e)}")
            return False, float('inf')

    def register_face(self, base64_image, name):
        """Register a new face"""
        try:
            image = self._process_base64_image(base64_image)
            face_roi = self._get_face_roi(image)

            if face_roi is None:
                return False, "No face or multiple faces detected in the image"

            # Check if face already exists
            for existing_face in self.known_faces:
                is_match, _ = self._compare_faces(face_roi, existing_face)
                if is_match:
                    return False, "This face is already registered"

            self.known_faces.append(face_roi)
            self.known_names.append(name)

            return True, "Face registered successfully"

        except Exception as e:
            logger.error(f"Error registering face: {str(e)}")
            return False, "Error during face registration"

    def verify_face(self, base64_image):
        """Verify a face against registered faces"""
        try:
            if not self.known_faces:
                return False, "No faces registered in the system"

            image = self._process_base64_image(base64_image)
            face_roi = self._get_face_roi(image)

            if face_roi is None:
                return False, "No face or multiple faces detected in the image"

            # Compare with all known faces
            min_error = float('inf')
            best_match_name = None

            for i, known_face in enumerate(self.known_faces):
                is_match, error = self._compare_faces(face_roi, known_face)
                if is_match and error < min_error:
                    min_error = error
                    best_match_name = self.known_names[i]

            if best_match_name:
                return True, best_match_name

            return False, "Face not recognized"

        except Exception as e:
            logger.error(f"Error verifying face: {str(e)}")
            return False, "Error during face verification"