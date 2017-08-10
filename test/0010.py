#! /usr/bin/env python
#! -*- coding: utf-8 -*-

__author__ = 'Sophie2805'

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
#from pylab import *
import random,numpy,string

path = "F://code"
# generate 4 ramdom letters
text = random.sample(string.ascii_letters,4)
#print text

# generate 3-D random array
rawArray = numpy.zeros((100,300,3),dtype=numpy.uint8)
sh = rawArray.shape
for i in range(sh[0]):
    for j in range(sh[1]):
        for k in range(sh[2]):
            rawArray[i][j][k]=random.randint(0,255)

# generate the background pic from 3-D array
im = Image.fromarray(rawArray)
draw = ImageDraw.Draw(im)

# add check code onto the background
for i in range(len(text)):
    draw.text((75*i+random.randint(0,40),random.randint(0,40)), text[i],
              font=ImageFont.truetype("Apple Symbols.ttc",60),
              fill = (random.randint(0,255),random.randint(0,255),random.randint(0,255)))

im.save(path+"/checkcode.jpg")
