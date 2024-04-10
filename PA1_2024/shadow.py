import numpy as np
from ray import Ray
from light import Light

class Shadow:
    def __init__(self, lights: list[Light]) -> None:
        self.lights = lights
        self.contribution = np.array([0.1, 0.1, 0.1])
        pass

    def shade(self, ray: Ray, t: float, normal: np.ndarray) -> np.ndarray:
        p = ray.origin + t * ray.direction
        
        