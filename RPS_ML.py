# Import libraries
import tkinter as tk
from tkinter.constants import DISABLED
import tkinter.font as font
from PIL import Image, ImageTk
import cv2
import tensorflow as tf
from keras.preprocessing import image as imageProcessing
import numpy as np
import random
import threading
import time

# Import TF model
model = tf.keras.models.load_model('model\\RPS_CNN.h5')

def ClassifyImage(image):

    # Random computer pick
    computer = random.randrange(0, 3)
    text = ""
    if(computer == 0):
        text = "Rock"
    elif(computer == 1):
        text = "Paper"
    else:
        text = "Scissor"

    # Output computer pick to text
    computerPick.config(state=tk.NORMAL)
    computerPick.delete(1.0, tk.END)
    computerPick.insert(1.0, 'I picked: ' + text)
    computerPick.tag_add("center", 1.0, tk.END)
    computerPick.config(state=DISABLED)

    # Load or take parameter image, put in array and let model predict
    # test.load_img('C:\\Users\\Mauri\\Repositories\\MachineLearning\\data\\rock.jpg', target_size=(300,300))
    image_src = image
    x = imageProcessing.img_to_array(image_src)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    classes = model.predict(images, batch_size=1)
    player = -1
    if classes[0, 0] == 1:
        text = "Rock"
        player = 0
    elif classes[0, 1] == 1:
        text = "Paper"
        player = 1
    elif classes[0, 2] == 1:
        text = "Scissor"
        player = 2

    # Output player's pick to text
    playerPick.config(state=tk.NORMAL)
    playerPick.delete(1.0, tk.END)
    playerPick.insert(1.0, "You've picked: " + text)
    playerPick.tag_add("center", 1.0, tk.END)
    playerPick.config(state=DISABLED)

    # Game logic
    message = ""
    adjusted = player - 1
    if adjusted < 0:
        adjusted = 2
    if player == computer:
        message = "Oh! A draw!"
    elif computer == adjusted:
        message = "You win!"
    else:
        message = "You lose!"

    # Output game result
    result.config(state=tk.NORMAL)
    result.delete(1.0, tk.END)
    result.insert(1.0, 'Game result: ' + message)
    result.tag_add("center", 1.0, tk.END)
    result.config(state=DISABLED)

# Extract image from camera stream

def Countdown():
    t = 3
    while t >= 0:
        min, sec = divmod(t, 60)
        countdown = '{:02d}:{:02d}'.format(min, sec)
        timer.config(state=tk.NORMAL)
        timer.delete(1.0, tk.END)
        timer.insert(1.0, countdown)
        timer.tag_add("center", 1.0, tk.END)
        timer.config(state=tk.DISABLED)
        window.update()
        time.sleep(1)
        t -= 1
    
    extract_stream_image()

def extract_stream_image():
    ret, frame = capture.read()
    frame = cv2.resize(frame, [300, 300])
    ClassifyImage(frame)
    # Save frame to disk
    #cv2.imwrite('Frame'+str(0)+'.jpg', frame)


# Setup window
window = tk.Tk()
window.geometry("900x500")
window.title("Rock, Paper, Machine")
window.configure(background='#323232')

#Logo
logo = ImageTk.PhotoImage(Image.open('logo.png'))
logoPanel = tk.Label(window, image=logo)
logoPanel.grid(row=0,column=1, columnspan=2, padx=100)

# Setup webcam capt/ure
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
capture.set(cv2.CAP_PROP_FPS, 60)

label = tk.Label(window)
label.grid(row=0, column=0, rowspan=3)

# Define function to show frame/camera stream


def show_frames():
    # Get camera frame
    cv2image = cv2.cvtColor(capture.read()[1], cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    # Convert to a PhotoImage
    imgtk = ImageTk.PhotoImage(image=img)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    # Repeat tp capture all the time
    label.after(10, show_frames)
 
# Create UI elements
myFont = font.Font(family='Bahnschrift')

# Start button
startButton = tk.Button(window, text='Play!', command=Countdown,
                        width=15, height=3, relief=tk.FLAT, bg='white')
startButton['font'] = myFont
startButton.grid(row=3, column=0, pady=65)


def CreateText(pWindow, pWidth, pHeight, pText, pRow, pColumn, pPadx=0, pPadY=0, pRowSpan=1, pColumnSpan=1):
    text = tk.Text(pWindow, width=pWidth, height=pHeight, relief=tk.FLAT)
    text['font'] = myFont
    text.insert(1.0, pText)
    text.tag_config("center", justify='center')
    text.grid(row=pRow, column=pColumn, padx=pPadx, pady=pPadY,
              rowspan=pRowSpan, columnspan=pColumnSpan)
    text.tag_add("center", 1.0, tk.END)
    text.config(state=DISABLED)
    return text


# Computer's pick text
computerPick = CreateText(window, 22, 2, "Let's play a game!", 2, 1)

# Player's pick text
playerPick = CreateText(window, 22, 2, "Here's what you've picked", 2, 2)

# Result text
result = CreateText(window, 22, 2, "Results will be here!", 3, 1, 0, 0, 1, 2)

# Timer text
#Set pady to 55 to align with camera window
timer = CreateText(window, 5, 1, "00:00", 1, 1, 0, 15, 1, 2)

show_frames()
window.mainloop()

# Release resources
capture.release()
cv2.destroyAllWindows()
