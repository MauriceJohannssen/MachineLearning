#Import libraries
import tkinter as tk
import tkinter.font as font
from PIL import Image, ImageTk
import cv2
import tensorflow as tf 
import tensorflow_datasets as tfds
from keras.preprocessing import image as test
import matplotlib.pyplot as plt
import numpy as np
import random

#Import TF model
model = tf.keras.models.load_model('C:\\Users\\Mauri\\Repositories\\MachineLearning\\model\\RPS_CNN.h5')

def ClassifyImage(image):
   
   computer = random.randrange(0,3)
   text = "";
   if(computer == 0): text = "Rock"
   elif(computer == 1):text = "Paper"
   else: text = "Scissor"

   gameText.delete(1.0, tk.END)
   gameText.insert(1.0, 'I picked: ' + text)

   image_src = image#test.load_img('C:\\Users\\Mauri\\Repositories\\MachineLearning\\data\\rock.jpg', target_size=(300,300))
   x = test.img_to_array(image_src)
   x = np.expand_dims(x, axis=0)
   images = np.vstack([x])
   classes = model.predict(images, batch_size=1)
   player = -1;
   if classes[0, 0] == 1:
      text = "Rock"
      player = 0
   elif classes[0, 1] == 1:
      text = "Paper"
      player = 1
   elif classes[0, 2] == 1:
      text = "Scissor"
      player = 2

   playerPick.delete(1.0, tk.END)
   playerPick.insert(1.0, "You've picked: " + text)
   
   message = ""
   adjusted = player - 1
   if adjusted < 0: 
      adjusted = 2;
   if player == computer: 
      message = "Oh! A draw!"
   elif computer == adjusted: 
      message = "You win!"
   else: 
      message = "You lose!"

   result.delete(1.0, tk.END)
   result.insert(1.0, message)

def extract_stream_image():
   ret, frame = capture.read()
   frame = cv2.resize(frame, [300,300])
   ClassifyImage(frame)
   # Save Frame by Frame into disk using imwrite method
   cv2.imwrite('Frame'+str(1)+'.jpg', frame)

#Setup window
window = tk.Tk()
window.geometry("900x500")
window.title("Rock, Paper, Scissor | Man vs. Machine")
window.configure(background='#323232')

label = tk.Label(window)
label.grid(row=0, column=0)

#Setup webcam capture
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
capture.set(cv2.CAP_PROP_FPS, 60)

#Create UI elements
myFont = font.Font(family='Bahnschrift')

startButton = tk.Button(window, text='Play!', 
command=extract_stream_image, width=10, height=10,relief=tk.FLAT, bg='white')
startButton['font'] = myFont
startButton.grid(row=1, column=0)

gameText = tk.Text(window, width=30, height=5)
gameText['font'] = myFont
gameText.insert(tk.INSERT, "Let's play a game!")
gameText.grid(row=0, column=1)

playerPick = tk.Text(window, width=30, height=5)
playerPick['font'] = myFont
playerPick.insert(tk.INSERT, "Here's what you've picked")
playerPick.grid(row=0, column=2)

result = tk.Text(window, width=30, height=5)
result['font'] = myFont
result.insert(tk.INSERT, "Results will be here!")
result.grid(row=1, column=0)

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

capture.release()
cv2.destroyAllWindows()