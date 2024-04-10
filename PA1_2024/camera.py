import numpy as np
from ray import Ray

class Camera:
    def __init__(self, viewPoint: np.ndarray, viewDir: np.ndarray, projNormal: np.ndarray, viewUp: np.ndarray, projDistance: float, viewWidth: float, viewHeight: float) -> None:
        self.viewPoint = viewPoint
        self.viewDir = viewDir
        self.projNormal = projNormal
        self.viewUp = viewUp
        self.projDistance = projDistance
        self.viewWidth = viewWidth
        self.viewHeight = viewHeight
        self.rays = []

    def createRays(self, imgSize: np.ndarray) -> None:
        u = np.cross(self.viewDir, self.viewUp)
        v = np.cross(u, self.viewDir)

        if np.linalg.norm(u) == 0:
            u_unit = np.array([0, 0, 0])
        else:
            u_unit = u / np.linalg.norm(u)

        if np.linalg.norm(v) == 0:
            v_unit = np.array([0, 0, 0])
        else:                      
            v_unit = v / np.linalg.norm(v)

        # print(u_unit, v_unit)

        pixel_w = self.viewWidth / imgSize[0]
        pixel_h = self.viewHeight / imgSize[1]
        # print(pixel_w, pixel_h)

        # u = l + (r - l) * (i + 0.5) / nx
        # v = b + (t - b) * (j + 0.5) / ny

        startPoint = (self.viewDir / np.linalg.norm(self.viewDir)) * self.projDistance + (-self.viewWidth / 2) * u_unit + (-self.viewHeight / 2) * v_unit + self.viewPoint
        startPoint += np.array([0.5 * pixel_w, 0.5 * pixel_h, 0])
        
        for i in range(imgSize[0]):
            temp = []
            for j in range(imgSize[1]):
                rayDirection = (startPoint + j * pixel_h * v_unit + i * pixel_w * u_unit) - self.viewPoint
                ray = Ray(self.viewPoint, rayDirection / np.linalg.norm(rayDirection))
                # print(ray.direction)
                temp.append(ray)
            self.rays.append(temp)
