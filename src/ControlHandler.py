
# Created by: Qingquan Zhao


import os
import cv2

class TrainImageHandler:
    def __init__(self, app):
        self.app = app

    def trainCascade(self):

        os.mkdir(self.app.parameters.data)
        os.mkdir(self.app.parameters.info)

        create_sample_cmd_1 = "opencv_createsamples -img {0} -bg {1} -info {2} -pngoutput {3} -maxxangle {4} -maxyangle {5} -maxzangle {6} -num {7}".format(self.app.imageToBeTrainedFileName,
                                                                                                                                                            self.app.parameters.bgTXT,
                                                                                                                                                            self.app.parameters.infoList,
                                                                                                                                                            self.app.parameters.info,
                                                                                                                                                            self.app.parameters.maxxangle,
                                                                                                                                                            self.app.parameters.maxyangle,
                                                                                                                                                            self.app.parameters.maxzangle,
                                                                                                                                                            self.app.parameters.negativeNum
                                                                                                                                                            )
        create_sample_cmd_2 = "opencv_createsamples -info {0} -num {1} -w {2} -h {3} -vec {4}".format(self.app.parameters.infoList,
                                                                                                        self.app.parameters.negativeNum,
                                                                                                        self.app.parameters.positiveImageWidth,
                                                                                                        self.app.parameters.positiveImageHeight,
                                                                                                        self.app.parameters.positiveVec
                                                                                                        )


        train_cascade_cmd_3 = "opencv_traincascade -data {0} -vec {1} -bg {2} -numPos {3} -numNeg {4} -numStages {5} -w {6} -h {7}".format(self.app.parameters.data,
                                                                                                                                        self.app.parameters.positiveVec,
                                                                                                                                        self.app.parameters.bgTXT,
                                                                                                                                        self.app.parameters.numPosForTrain,
                                                                                                                                        self.app.parameters.numNegativeForTrain,
                                                                                                                                        self.app.parameters.numStages,
                                                                                                                                        self.app.parameters.positiveImageWidth,
                                                                                                                                        self.app.parameters.positiveImageHeight
                                                                                                                                         )

        os.system(create_sample_cmd_1)
        os.system(create_sample_cmd_2)
        os.system(train_cascade_cmd_3)


class TestHandler:

    def __init__(self, app):
        self.app = app

    def testVideo(self):
        currentCascadeFile = cv2.CascadeClassifier(self.app.cascadeFilePath)
        try:
            capture = cv2.VideoCapture(0)
        except Exception:
            self.app.videoDetectionMessage['text'] = "No Camera Detected"
            return

        while True:
            _, img = capture.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            targetObject = currentCascadeFile.detectMultiScale(gray, 2.2, 8)
            for (x, y, w, h) in targetObject:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imshow('Press ESC to quit', img)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        capture.release()
        cv2.destroyAllWindows()


    def testImage(self, imageToBeDetectedPath):
        imageBeforeDetection = cv2.imread(imageToBeDetectedPath, 1)
        currentCascadeFile = cv2.CascadeClassifier(self.app.cascadeFilePath)
        templateImage = cv2.imread(self.app.imageToBeTrainedPath, 1)
        imageAfterDetection = self._imageDetectAlgorithmsVersion1(imageBeforeDetection, templateImage, currentCascadeFile)
        cv2.imshow('Press ECS to quit', imageAfterDetection)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def _imageDetectAlgorithmsVersion1(self, imageBeforeDetection, templateImage, cascadeFile):
        # Using cascadeFile to detect potential boxes, and stored in candidates, elements of which is (x, y, w, h)
        grayImageToBeDetected = cv2.cvtColor(imageBeforeDetection, cv2.COLOR_BGR2GRAY)
        candidates = list()
        for i in [3.5, 2.5, 2, 1.5, 1.1]:
            for j in [9, 8, 7, 6, 5]:
                targetObject = cascadeFile.detectMultiScale(grayImageToBeDetected, i, j)
                for (x, y, w, h) in targetObject:
                    candidates.append((x, y, w, h))

        # Obtain locations of matched features in full picture. Store these locations in a list
        grayTemplateImage = cv2.cvtColor(templateImage, cv2.COLOR_BGR2GRAY)
        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(grayTemplateImage, None)
        kp2, des2 = sift.detectAndCompute(grayImageToBeDetected, None)
        bf = cv2.BFMatcher()
        matches = bf.match(des2, des1)
        matchedFeatureLocationList = list()
        for matchedLocation in matches:
            idx = matchedLocation.queryIdx
            x, y = kp2[idx].pt
            x = int(x)
            y = int(y)
            matchedFeatureLocationList.append((x, y))

         # Determine which box is the best based on feature matching numbers in it.
        maxNum = 0
        maxLocation = (0, 0, 0, 0)
        for box in candidates:
            inBoxNum = 0
            for splotLocation in matchedFeatureLocationList:
                if self.inBox(box, splotLocation):
                    inBoxNum += 1
            if inBoxNum > maxNum:
                maxNum = inBoxNum
                maxLocation = box

        # draw maxLocation on Image and return new Image
        (max_x, max_y, max_w, max_h) = maxLocation
        cv2.rectangle(imageBeforeDetection, (max_x, max_y), (max_x + max_w, max_y + max_h), (255, 0, 0), 3)
        return imageBeforeDetection

    def inBox(self, box, location):
        x, y, w, h = box
        a, b = location
        if a > x and a < x+w and b > y and b < y+h:
            return True
        return False
