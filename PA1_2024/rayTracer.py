#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image 

from surfaces import Sphere, Box
from shaders import Shader, ShaderPhong, ShaderLambertian
from camera import Camera
from light import Light
from ray import Ray
from surfaces import Surface

class Color:
    def __init__(self, R, G, B):
        self.color=np.array([R,G,B]).astype(np.float64)

    def __init__(self, color: np.ndarray):
        self.color=color.astype(np.float64)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma;
        self.color=np.power(self.color, inverseGamma)
        return self

    def toUINT8(self):
        return (np.clip(self.color, 0,1)*255).astype(np.uint8)
    
def elementToSurface(element):
    # pdb.set_trace()
    if element.get('type') == 'Sphere':
        center = np.array(element.find('center').text.split()).astype(np.float64)
        radius = float(element.find('radius').text)
        return Sphere(element.find('shader').get('ref'), center, radius)
    elif element.get('type') == 'Box':
        minPt = np.array(element.find('minPt').text.split()).astype(np.float64)
        maxPt = np.array(element.find('maxPt').text.split()).astype(np.float64)

        return Box(element.find('shader').get('ref'), minPt, maxPt)

def elementToShaderTuple(element, lights):
    if element.get('type') == 'Phong':
        diffuseColor = np.array(element.find('diffuseColor').text.split()).astype(np.float64)
        specularColor = np.array(element.find('specularColor').text.split()).astype(np.float64)
        exponent = float(element.find('exponent').text)
        return (element.get('name'), ShaderPhong(lights, diffuseColor, specularColor, exponent))
    
    elif element.get('type') == 'Lambertian':
        diffuseColor = np.array(element.find('diffuseColor').text.split()).astype(np.float64)
        return (element.get('name'), ShaderLambertian(lights, diffuseColor))
    
def elementToLight(element):
    intensity = np.array(element.find('intensity').text.split()).astype(np.float64)
    position = np.array(element.find('position').text.split()).astype(np.float64)
    return Light(position, intensity)

def trace(ray: Ray, surfaces: list):
    tmin = np.inf
    hitSurface = None
    for surface in surfaces:
        t = surface.intersect(ray)
        if t < tmin:
            tmin = t
            hitSurface = surface
    return tmin, hitSurface

def shade(ray: Ray, tmin: float, shaders: dict, hitSurface: Surface, surfaces: list):
    p = ray.origin + tmin * ray.direction
    if tmin < np.inf:
        return Color(shaders[hitSurface.shaderName].shade(ray, tmin, hitSurface.normal(p), hitSurface, surfaces)).gammaCorrect(2.2).toUINT8()
    else:
        return Color(np.zeros(3)).toUINT8()

def main():
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    lights = list(map(lambda x : elementToLight(x), root.findall('light')))
    shaders = dict(tuple(map(lambda x : elementToShaderTuple(x, lights), root.findall('shader'))))
    surfaces = list(map(lambda x : elementToSurface(x) ,root.findall('surface')))

    # pdb.set_trace()

    viewPoint = np.array(root.find('camera').find('viewPoint').text.split()).astype(np.float64)
    viewDir = np.array(root.find('camera').find('viewDir').text.split()).astype(np.float64)
    projNoraml = np.array(root.find('camera').find('projNormal').text.split()).astype(np.float64)
    viewProjNormal=-1*viewDir  # you can safely assume this. (no examples will use shifted perspective camera)
    viewUp = np.array(root.find('camera').find('viewUp').text.split()).astype(np.float64)
    projDistance = float(root.find('camera').find('projDistance').text)
    viewWidth = float(root.find('camera').find('viewWidth').text)
    viewHeight = float(root.find('camera').find('viewHeight').text)

    imgSize=np.array(root.findtext('image').split()).astype(np.int32)
    print('imgSize', imgSize)

    camera = Camera(viewPoint, viewDir, projNoraml, viewUp, projDistance, viewWidth, viewHeight)
    camera.createRays(imgSize)

    #code.interact(local=dict(globals(), **locals()))  

    # Create an empty image
    channels=3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:,:]=0

    for i in np.arange(imgSize[1]):
        for j in np.arange(imgSize[0]):
            ray = camera.rays[j][i]
            tmin, hitSurface = trace(ray, surfaces)
            img[imgSize[1] - i - 1][j] = shade(ray, tmin, shaders, hitSurface, surfaces)

    # save the image
    rawimg = Image.fromarray(img, 'RGB')
    #rawimg.save('out.png')
    rawimg.save(sys.argv[1]+'.png')
    
if __name__=="__main__":
    main()
