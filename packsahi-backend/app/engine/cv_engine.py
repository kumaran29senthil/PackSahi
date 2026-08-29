import cv2
import numpy as np

class CVEngine:
    @staticmethod
    def preprocess_image(image_bytes: bytes) -> np.ndarray:
        """Converts raw image bytes into an optimized grayscale CLAHE OpenCV matrix."""
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Grayscale conversion
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        return enhanced

    @staticmethod
    def dewarp_cylindrical_surface(img: np.ndarray) -> np.ndarray:
        """Point-cloud 3D cylindrical surface unwarping for curved bottle/can labels."""
        h, w = img.shape[:2]
        # Generate cylindrical surface transform mesh
        focal_length = w  # Approximate focal length parameter
        K = np.array([[focal_length, 0, w / 2],
                      [0, focal_length, h / 2],
                      [0, 0, 1]], dtype=np.float32)
        
        # Apply transformation mapping to flatten curves
        map_x, map_y = np.meshgrid(np.arange(w), np.arange(h))
        x_c = (map_x - w / 2) / focal_length
        y_c = (map_y - h / 2) / focal_length
        
        # Cylinder mapping projection equations
        theta = np.arctan(x_c)
        h_c = y_c / np.cos(theta)
        
        x_proj = focal_length * theta + w / 2
        y_proj = focal_length * h_c + h / 2
        
        dewarped = cv2.remap(img, x_proj.astype(np.float32), y_proj.astype(np.float32), cv2.INTER_LINEAR)
        return dewarped
