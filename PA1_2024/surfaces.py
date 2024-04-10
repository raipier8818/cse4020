import numpy as np
from ray import Ray

class Surface:
    def __init__(self, shaderName: str) -> None:
        self.shaderName = shaderName
        pass

    def intersect(self, ray: Ray) -> float:
        pass

    def normal(self, point: np.ndarray) -> np.ndarray:
        pass

    def shade(self, ray: Ray, t: float) -> np.ndarray:
        pass


class Sphere(Surface):
    def __init__(self, shaderName: str, center: np.ndarray, radius: float) -> None:
        super().__init__(shaderName)
        self.center = center
        self.radius = radius
    
    def intersect(self, ray: Ray) -> float:
        # (p + td - c) . (p + td - c) = r^2
        d = ray.direction
        p = ray.origin
        c = self.center
        r = self.radius

        a = np.dot(d, d)
        b = 2 * np.dot(d, p - c)
        c = np.dot(p - c, p - c) - r**2

        discriminant = b**2 - 4 * a * c
        if discriminant >= 0:
            t1 = (-b + np.sqrt(discriminant)) / (2 * a)
            t2 = (-b - np.sqrt(discriminant)) / (2 * a)
            t = min(t1, t2)
            return t
        else:
            return np.inf
        
    def normal(self, point: np.ndarray) -> np.ndarray:
        return (point - self.center) / self.radius
    
    def shade(self, ray: Ray, t: float) -> np.ndarray:
        point = ray.origin + t * ray.direction
        normal = self.normal(point)
        return self.shader.shade(ray, t, normal)

class Box(Surface):
    def __init__(self, shaderName: str, minPt: np.ndarray, maxPt: np.ndarray) -> None:
        super().__init__(shaderName)
        self.minPt = minPt
        self.maxPt = maxPt
    
    def intersect(self, ray: Ray) -> float:
        # if np.linalg.norm(ray.origin - self.minPt) > np.linalg.norm(ray.origin - self.maxPt):
        #     self.minPt, self.maxPt = self.maxPt, self.minPt

        # ray.direction -= ray.origin
        if ray.direction[0] != 0:
            txmin = (self.minPt[0] - ray.origin[0]) / ray.direction[0]
            txmax = (self.maxPt[0] - ray.origin[0]) / ray.direction[0]
            tx_min = min(txmin, txmax)
            tx_max = max(txmin, txmax)
        else:
            tx_min = -np.inf
            tx_max = np.inf

        if ray.direction[1] != 0:
            tymin = (self.minPt[1] - ray.origin[1]) / ray.direction[1]
            tymax = (self.maxPt[1] - ray.origin[1]) / ray.direction[1]
            ty_min = min(tymin, tymax)
            ty_max = max(tymin, tymax)
        else:
            ty_min = -np.inf
            ty_max = np.inf

        if ray.direction[2] != 0:
            tzmin = (self.minPt[2] - ray.origin[2]) / ray.direction[2]
            tzmax = (self.maxPt[2] - ray.origin[2]) / ray.direction[2]
            tz_min = min(tzmin, tzmax)
            tz_max = max(tzmin, tzmax)
        else:
            tz_min = -np.inf
            tz_max = np.inf
        # print(txmin, txmax, tymin, tymax, tzmin, tzmax)
        tmin = max(tx_min, ty_min, tz_min)
        tmax = min(tx_max, ty_max, tz_max)

        # print(tmin, tmax)
        
        if tmin > tmax:
            return np.inf
        else:
            # print(tmin)
            return tmin
        
    def normal(self, point: np.ndarray) -> np.ndarray:
        if np.isclose(point[0], self.minPt[0]):
            return np.array([-1, 0, 0])
        elif np.isclose(point[0], self.maxPt[0]):
            return np.array([1, 0, 0])
        elif np.isclose(point[1], self.minPt[1]):
            return np.array([0, -1, 0])
        elif np.isclose(point[1], self.maxPt[1]):
            return np.array([0, 1, 0])
        elif np.isclose(point[2], self.minPt[2]):
            return np.array([0, 0, -1])
        elif np.isclose(point[2], self.maxPt[2]):
            return np.array([0, 0, 1])
