from ray import Ray
import numpy as np
from light import Light
from surfaces import Surface

class Shader:
    def __init__(self, lights: list) -> None:
        self.lights = lights
        pass

    def shade(self, ray: Ray, t: float, normal: np.ndarray, hitSurface: Surface, surfaces: list) -> np.ndarray:
        pass

class ShaderPhong(Shader):
    def __init__(self, lights, diffuseColor: np.ndarray, specularColor: np.ndarray, exponent: float) -> None:
        super().__init__(lights)
        self.diffuseColor = diffuseColor
        self.specularColor = specularColor
        self.exponent = exponent
    
    def shadow(self, ray: Ray, t: float, light: Ray, hitSurface: Surface, surfaces: list) -> bool:
        p = ray.origin + t * ray.direction
        for surface in surfaces:
            if surface != hitSurface:
                t_shadow = surface.intersect(Ray(p, light.position - p))
                if 0 < t_shadow < np.inf:
                    return True
        return False
    
    def shade(self, ray: Ray, t: float, normal: np.ndarray, hitSurface: Surface, surfaces: list) -> np.ndarray:
        #L_s = k_s * I * max(0, n . h)^p
        p = ray.origin + t * ray.direction
        L_s = np.zeros(3)
        

        for light in self.lights:
            if self.shadow(ray, t, light, hitSurface, surfaces):
                continue

            l = light.position - p
            l_unit = l / np.linalg.norm(l)
            n_unit = normal / np.linalg.norm(normal)
            if np.linalg.norm(l_unit - ray.direction) == 0:
                h = np.array([0, 0, 0])
            else:
                h = (l_unit - ray.direction) / np.linalg.norm(l_unit - ray.direction)
            L_s += self.specularColor * light.intensity * (max(0, np.dot(n_unit, h))**self.exponent)
            L_s += self.diffuseColor * light.intensity * max(0, np.dot(n_unit, l_unit))

        return L_s
        
class ShaderLambertian(Shader):
    def __init__(self, lights, diffuseColor: np.ndarray) -> None:
        super().__init__(lights)
        self.diffuseColor = diffuseColor

    def shadow(self, ray: Ray, t: float, light: Ray, hitSurface: Surface, surfaces: list) -> bool:
        p = ray.origin + t * ray.direction
        for surface in surfaces:
            if surface != hitSurface:
                t_shadow = surface.intersect(Ray(p, light.position - p))
                if 0 < t_shadow < np.inf:
                    return True
        return False
    
    def shade(self, ray: Ray, t: float, normal: np.ndarray, hitSurface: Surface, surfaces: list) -> np.ndarray:
        p = ray.origin + t * ray.direction
        L_d = np.zeros(3)
        for light in self.lights:
            if self.shadow(ray, t, light, hitSurface, surfaces):
                continue
            l = light.position - p
            l_unit = l / np.linalg.norm(l)
            n_unit = normal / np.linalg.norm(normal)
            L_d += self.diffuseColor * light.intensity * max(0, np.dot(n_unit, l_unit))
        return L_d
        
    