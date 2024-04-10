import numpy as np
from ray import Ray

class Light:
    def __init__(self, position: np.ndarray, intensity: np.ndarray) -> None:
        self.position = position
        self.intensity = intensity
        self.ambient = np.array([0.1, 0.1, 0.1])

    def ray(self, point: np.ndarray) -> np.ndarray:
        return Ray(point, (self.position - point) / np.linalg.norm(self.position - point))