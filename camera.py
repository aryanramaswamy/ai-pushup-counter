import cv2 as cv

class Camera:
    def __init__(self):
        self.camera = cv.VideoCapture(0) #0 is for default camera
        if not self.camera.isOpened():
            raise Exception("Could not open camera")
        
        self.width = int(self.camera.get(cv.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.camera.get(cv.CAP_PROP_FRAME_HEIGHT))

    def getFrame(self):
        if self.camera.isOpened():
            ret, frame = self.camera.read()
            if not ret:
                return (ret, None)
            else:
                return (ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB))
        else:
            return (False, None)

    def __del__(self):
        if self.camera.isOpened():
            self.camera.release()
