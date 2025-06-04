import cv2
import numpy as np
import PIL.Image
from sklearn.svm import LinearSVC
import pickle
import os
import joblib

class Model:
    def __init__(self):
        try:
            self.model = joblib.load("pushup_model.pkl")
            self.trained = True
            print("Loaded saved model.")
        except:
            self.model = LinearSVC()
            self.trained = False
            print("No saved model found. Please train the model first.")

    def trainModel(self):
        imgList = []
        groupList = []

        for file in os.listdir("1"):
            path = os.path.join("1", file)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (150, 150))
            img = img.reshape(-1)
            imgList.append(img)
            groupList.append(1)

        for file in os.listdir("2"):
            path = os.path.join("2", file)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (150, 150))
            img = img.reshape(-1)
            imgList.append(img)
            groupList.append(2)

        X = np.array(imgList)
        y = np.array(groupList)

        self.model.fit(X, y)
        joblib.dump(self.model, "pushup_model.pkl")
        self.trained = True
        print("Model trained with image dataset!")



    def saveModel(self):
        if self.trained:
            with open('trained_model.pkl', 'wb') as f:
                pickle.dump(self.model, f)
            print("Model saved successfully")

    def loadModel(self):
        try:
            with open('trained_model.pkl', 'rb') as f:
                self.model = pickle.load(f)
            self.trained = True
            print("Model loaded successfully")
        except FileNotFoundError:
            print("No saved model found. Please train the model first.")
            self.trained = False

    def predict(self, frame):
        if not self.trained:
            print("Model is not trained yet.")
            return 0  # Default or "neutral" position
        frame = frame[1]
        #save temporary frame
        cv2.imwrite("temp.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

        #resize and convert to grayscale
        img = PIL.Image.open("temp.jpg")
        img = img.resize((150, 150))
        img.save("temp.jpg")
        img = cv2.imread("temp.jpg", cv2.IMREAD_GRAYSCALE)
        img = img.reshape(1, -1) #flatten and make 2d

        prediction = self.model.predict(img)
        return prediction[0]
