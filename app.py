import tkinter as tk
import os
import PIL.Image, PIL.ImageTk
import cv2
import camera
import model

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("AI Push-Up Rep Counter")

        # Initialize components
        self.repCounter = 0
        self.up = False
        self.down = False
        self.lastPosition = 0

        self.model = model.Model()
        self.camera = camera.Camera()
        self.countingEnabled = False

        self.init_gui()

        self.delay = 15
        self.update()

        self.window.mainloop()

    def init_gui(self):
        # === Create Layout Frames ===
        self.canvas_frame = tk.Frame(self.window)
        self.canvas_frame.pack()

        self.controls_frame = tk.Frame(self.window)
        self.controls_frame.pack()

        # === Canvas Display ===
        self.canvas = tk.Canvas(self.canvas_frame, width=self.camera.width, height=self.camera.height)
        self.canvas.pack()

        # === Rep Counter Display ===
        self.counterLabel = tk.Label(self.controls_frame, text=f"{self.repCounter} Reps", font=("Courier", 40))
        self.counterLabel.pack(anchor=tk.CENTER, pady=10)

        # === Control Buttons ===
        self.btn_toggle = tk.Button(self.controls_frame, text="Toggle Counting", width=50, command=self.toggleCounting)
        self.btn_toggle.pack(anchor=tk.CENTER)

        self.btn_up = tk.Button(self.controls_frame, text="Save Up Position", width=50, command=lambda: self.saveForGroup(1))
        self.btn_up.pack(anchor=tk.CENTER)

        self.btn_down = tk.Button(self.controls_frame, text="Save Down Position", width=50, command=lambda: self.saveForGroup(2))
        self.btn_down.pack(anchor=tk.CENTER)

        self.btn_train = tk.Button(self.controls_frame, text="Train Model", width=50, command=self.model.trainModel)
        self.btn_train.pack(anchor=tk.CENTER)

        self.btn_reset = tk.Button(self.controls_frame, text="Reset Reps", width=50, command=self.resetCounter)
        self.btn_reset.pack(anchor=tk.CENTER)


    def update(self):
        if self.countingEnabled:
            self.predict()

        # Count a rep only if full cycle: Down -> Up
        if self.lastPosition == 2 and self.up:
            self.repCounter += 1
            self.up = False


        self.counterLabel.config(text=f"{self.repCounter} Reps")

        ret, frame = self.camera.getFrame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def predict(self):
        frame = self.camera.getFrame()
        prediction = self.model.predict(frame)

        if prediction != self.lastPosition:
            if prediction == 1:
                self.up = True
            elif prediction == 2:
                self.down = True
            self.lastPosition = prediction


    def toggleCounting(self):
        self.countingEnabled = not self.countingEnabled

    def resetCounter(self):
        self.repCounter = 0
