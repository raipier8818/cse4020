import numpy as np
class Ray:
    def __init__(self, origin: np.ndarray, direction: np.ndarray) -> None:
        self.origin = origin
        self.direction = direction / np.linalg.norm(direction)
        pass