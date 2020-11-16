import os
import mysql.connector
import csv
import python_speech_features as mfcc
from sklearn import preprocessing
import warnings
import librosa
from keras.optimizers import SGD
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import numpy as np
from keras import layers
from keras import models
from keras import optimizers
from keras import regularizers
from keras import losses
from keras.callbacks import ModelCheckpoint,EarlyStopping
import librosa
import librosa.display
from scipy.fftpack import fft,fftfreq
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard
import IPython.display as ipd
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import Adam
from keras.utils import np_utils
from sklearn import metrics

def get_MFCC(audio,sr):
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    mfccs_processed = np.mean(mfccs.T,axis=0)
    print(mfccs_processed.shape)
    return mfccs_processed

model = Sequential()
db = mysql.connector.connect(host = 'localhost' , user = 'root' , passwd = 'root')
my = db.cursor()
my.execute('use Voice_Comparer')
sql = 'select * from Student_Data_By_Path where StudentID = %s'
val = (317126510024,)
my.execute(sql,val,)
res = my.fetchall()
path = []
Label = []
for i in res :
    path.append(i[1])
    Label.append(i[2])
set_Labels = list(set(Label))
Train_audio = []
Train_label = []
epochs = 50
duration = 30
sr = 22050
batch_size = 32
for i in path :
    data , sr = librosa.load(i,res_type='kaiser_best')
    Train_audio.append(get_MFCC(data,sr))
for i in Label :
    Train_label.append(set_Labels.index(i))
num_labels = len(set_Labels)
Train_audio = np.array(Train_audio)
Train_label = np.array(Train_label,dtype=np.int)
activation_fn = 'glorot_normal'
model.add(layers.Dense(256,input_shape=Train_audio[0].shape,activation='tanh'))
model.add(Dropout(.3))
model.add(layers.Dense(64,activation='tanh'))
model.add(Dropout(.3))
model.add(layers.Dense(num_labels,init=activation_fn))
model.add(Activation('softmax'))
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='sparse_categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])
model.summary()
history = model.fit(Train_audio,Train_label,epochs=epochs,validation_split=.2,batch_size=batch_size)
print(history.history.keys())
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
Test_File = ''
while 1 :
    Test_File = input('Enter Location : ')
    if Test_File == 'q' :
        exit()
    audio=[]
    data,sr = librosa.core.load(Test_File,res_type='kaiser_best')
    audio.append(get_MFCC(data,sr))
    audio = np.array(audio)
    pred = model.predict(audio)
    print(" ==>> " + str(pred) , ' - ' , str(pred.argmax(-1)) , set_Labels[pred.argmax(axis=-1)[0]] )
