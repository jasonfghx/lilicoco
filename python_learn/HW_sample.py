# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 00:37:00 2019

@author: user
"""

import os
import cv2    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import Image
from keras.preprocessing import image
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from PIL import Image





train_data_path = './train/'
test_data_path = './testset/'

labels = []
images = []
labels_hot =[]
dict_hot={"bedroom":0,
          'CALsuburb':1,
          'coast':2,
          'forest':3,
          'highway':4,
          'industrial':5,
          'insidecity':6,
          'kitchen':7,
          'livingroom':8,
          'mountain':9,
          'opencountry':10,
          'PARoffice':11,
          'store':12,
          'street':13,
          'tallbuilding':14,
          }
for root, dirs, files in os.walk(train_data_path):
    if len(files) >0 and ('ipynb_checkpoints' not in root): 
        for f in files:
            p = root.split('/')
            r = p[-1]
            labels.append(r)
            labels_hot.append(dict_hot[r])
            file = root + '/' + f
            img = image.load_img(file)
#            img = img.convert('L')
            img = img.resize( (128, 128))       
            img = img_to_array(img)
            images.append(img)
#s=np.expand_dims(images[0], axis=2)
#plt.imshow(images[0])
#plt.show()
images=np.array(images)
#plt.imshow(images[4])
#plt.show()
images=images.astype('float32')/255
labels_hot=np.array(labels_hot)
#print(images[1].shape)
##print(labels)
#print(labels_hot.shape)
#
#
from keras.utils import np_utils
Y = np_utils.to_categorical(labels_hot)
#print(Y)
#
#from sklearn.utils import shuffle
#x,y = shuffle(images,Y, random_state=2)
##print(x.shape)
##print(y.shape)
from sklearn.model_selection import train_test_split
X_train, X_valid, Y_train, Y_valid = train_test_split(images,Y, test_size=0.25, random_state=2)
#plt.imshow(X_train[1],cmap='gray')
#plt.show()

#print(X_train.shape)
#print(X_valid.shape)
#print(Y_train.shape)
#print(Y_valid.shape)
#
#
#
#
#
#
#
from keras.models import Sequential
from keras.layers import Dense,Dropout,Activation,Flatten
from keras.layers import Conv2D,MaxPooling2D,ZeroPadding2D
model=Sequential()

#第一次卷積
model.add(Conv2D(filters=32,
                 kernel_size=(3,3),
                 input_shape=(128,128,3),
                 activation='relu',
                 padding='same'))

model.add(Conv2D(filters=32,
                 kernel_size=(3,3),
                 activation='relu',
                 padding='same'))

#第一次池化
model.add(MaxPooling2D(pool_size=(2,2)))

#斷開25%連接
model.add(Dropout(0.25))
#並加入第二次卷積
model.add(Conv2D(filters=64,
                 kernel_size=(3,3),
                 activation='relu',
                 padding='same'))
model.add(Conv2D(filters=64,
                 kernel_size=(3,3),
                 activation='relu',
                 padding='same'))
#以及第二次池化
model.add(MaxPooling2D(pool_size=(2,2)))
#斷開25%連接
model.add(Dropout(0.25))
###
####並加入第三次卷積
model.add(Conv2D(filters=128,
                 kernel_size=(3,3),
                 activation='relu',
                 padding='same'))
model.add(Conv2D(filters=128,
                 kernel_size=(3,3),
                 activation='relu',
                 padding='same'))
####以及第三次池化
model.add(MaxPooling2D(pool_size=(2,2)))
#
##斷開25%連接
#model.add(Dropout(0.25))
###以及第四次池化
#model.add(Conv2D(filters=256,
#                 kernel_size=(3,3),
#                 activation='relu',
#                 padding='same'))
#model.add(Conv2D(filters=256,
#                 kernel_size=(3,3),
#                 activation='relu',
#                 padding='same'))
#model.add(MaxPooling2D(pool_size=(2,2)))
##斷開25%連接
#model.add(Dropout(0.25))
###以及第五次池化
#model.add(Conv2D(filters=512,
#                 kernel_size=(3,3),
#                 activation='relu',
#                 padding='same'))
#model.add(Conv2D(filters=512,
#                 kernel_size=(3,3),
#                 activation='relu',
#                 padding='same'))
#model.add(MaxPooling2D(pool_size=(2,2)))


#model.add(Conv2D(filters=128,
#                 kernel_size=(3,3),
#                 activation='relu',
#                 padding='same'))
#model.add(Conv2D(filters=2048,
#                 kernel_size=(3,3),
#                 activation='relu',
#                 padding='same'))
#model.add(MaxPooling2D(pool_size=(2,2)))

##把處理過的東西攤開成一維
model.add(Flatten())
model.add(Dropout(rate=0.25))
#
##全連接層
model.add(Dense(128,activation='relu'))
model.add(Dropout(rate=0.25))
#model.add(Dense(1024,activation='relu'))
#model.add(Dropout(rate=0.25))
model.add(Dense(15,activation='softmax'))


print(model.summary())


from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
display(SVG(model_to_dot(model).create(prog='dot',format='svg')))


model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
train_history=model.fit(x=X_train,y=Y_train,
                        validation_split=0.1,
                        epochs=15,
                        batch_size=70,
                        verbose=2)


#plt.plot(train_history.history['loss'])
#plt.plot(train_history.history['val_loss'])
#plt.title('Loss Graph')
#plt.legend(['loss','val_loss'],loc='upper left')
#plt.show()
#

