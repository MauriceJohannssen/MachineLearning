#Import libraries
import tkinter as tk
import tkinter.font as font
from PIL import Image, ImageTk
import cv2
import os
import tensorflow as tf 
import tensorflow_datasets as tfds
from keras.preprocessing import image as test
import matplotlib.pyplot as plt
import numpy as np
import platform

#Import TF model
model = tf.keras.models.load_model('RPS_CNN.h5')

def ClassifyImage():
   image_src = test.load_img('C:\\Users\\Mauri\\Repositories\\MachineLearning\\data\\rock.jpg', target_size=(300,300))
   x = test.img_to_array(image_src)
   x = np.expand_dims(x, axis=0)
   images = np.vstack([x])
   classes = model.predict(images, batch_size=1)
   if classes[0, 0] == 1:
      print('rock')
   elif classes[0, 1] == 1:
      print('paper')
   elif classes[0, 2] == 1:s
      print('scissors')

ClassifyImage()

#Setup window
window = tk.Tk()
window.geometry("900x500")
window.title("Rock, Paper, Scissor | Man vs. Machine")
window.configure(background='#323232')

#This is just for saving camera frames
imagePath = r'C:\\Users\\Mauri\\Desktop'
fileName = "testImage.jpg"
os.chdir(imagePath)

label = tk.Label(window)
label.grid(row=0, column=0)

#Setup webcam capture
capture = cv2.VideoCapture(0)
width, height = 360, 240
capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
capture.set(cv2.CAP_PROP_FPS, 60)

print(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
print(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

#Create UI elements
myFont = font.Font(family='Bahnschrift')

startButton = tk.Button(window, text='Play!', 
command=ClassifyImage, width=10, height=10,relief=tk.FLAT, bg='white')
startButton['font'] = myFont
startButton.grid(row=1, column=0)

gameText = tk.Text(window, width=30, height=5)
gameText['font'] = myFont
gameText.insert(tk.INSERT, 'This is an example text')
gameText.grid(row=0, column=1)


# Define function to show frame
def show_frames():
   #Get camera frame
   cv2image= cv2.cvtColor(capture.read()[1],cv2.COLOR_BGR2RGB)
   img = Image.fromarray(cv2image)
   #Convert to a PhotoImage
   imgtk = ImageTk.PhotoImage(image = img)
   label.imgtk = imgtk
   label.configure(image=imgtk)
   #Repeat tp capture all the time
   label.after(10, show_frames)


show_frames()
window.mainloop()