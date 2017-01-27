
# Created by: Qingquan Zhao

from tkinter import *
import tkinter.filedialog as filedialog
import platform
import os

class Parameters():

    def __init__(self, appMain):
        self.appMain = appMain
        self.root = appMain.root
        self._setDefaultValues()

    def _setDefaultNegativePath(self):
        if str(platform.system()) == 'darwin':
            self.negativePath = "neg"
        else:
            self.negativePath = "neg"

    def _setDefaultDirectoryBasedOnSystem(self):
        if str(platform.system()) == 'darwin':
            self.positiveVec = "positives.vec"
            self.info = "info"
            self.data = "data"
            self.bgTXT = "bg.txt"
            self.infoList = "info\\info.lst"
        else:
            self.positiveVec = "positives.vec"
            self.info = "info"
            self.data = "data"
            self.bgTXT = "bg.txt"
            self.infoList = "info/info.lst"
        self._setDefaultNegativePath()

    def _getForbiddenDirectoryAndFileSet(self):
        return [self.info, self.data, self.bgTXT, self.positiveVec, self.infoList]

    def _setDefaultValues(self):
        self._setDefaultDirectoryBasedOnSystem()
        # parameters for creating samples
        self.maxxangle = 0.5
        self.maxyangle = 0.5
        self.maxzangle = 0.5
        self.negativeNum = 1900
        self.positiveNum = 1900
        self.positiveImageWidth = 20
        self.positiveImageHeight = 20

        # parameters for training
        self.numPosForTrain = (self.positiveNum * 9)//10
        self.numNegativeForTrain = self.numPosForTrain//2
        self.numStages = 10

    def initiateGUI(self):

        self.ParametersPanelFrame = Frame(self.root)
        self.ParametersPanelFrame.pack()

        self._drawSpace()
        self.title = Label(self.ParametersPanelFrame, text = 'Parameters Settings', fg="red", font=("Helvetica", 20), anchor=CENTER)
        self.title.pack(side = TOP)
        self._drawHorizontalLine()

        self.ParamFrame = Frame(self.ParametersPanelFrame)
        self.ParamFrame.pack()

        # Negative Folder GUI
        self.setNegativePathLabel = Label(self.ParamFrame, text = "Background Image Folder:", fg="blue", font=("Helvetica", 14)).grid(columnspan = 2, column=0, row=0)
        self.setNegativePathButton = Button(self.ParamFrame, text = "Choose", command=self._chooseImage)
        self.setNegativePathButton.grid(columnspan = 3, column=2, row=0)
        self.chooseImageMessage = Label(self.ParamFrame, text = "", fg="red", font=("Helvetica", 12))
        self.chooseImageMessage.grid(columnspan = 2, column=5, row=0)

        # set max angle GUI
        self.maxAngleLabel = Label(self.ParamFrame, text = "Max Angle:   x:", fg="blue", font=("Helvetica", 14)).grid(column=0, row=2)
            # x
        self.maxxangleEntry = Entry(self.ParamFrame, width = 3)
        self.maxxangleEntry.insert(0, "0.5")
        self.maxxangleEntry.grid(column=1, row=2)
            # y
        self.maxYAngleLabel = Label(self.ParamFrame, text = "y: ", fg="blue", font=("Helvetica", 14)).grid(column=2, row=2)
        self.maxyangleEntry = Entry(self.ParamFrame, width = 3)
        self.maxyangleEntry.insert(0, "0.5")
        self.maxyangleEntry.grid(column=3, row=2)
            # z
        self.maxZAngleLabel = Label(self.ParamFrame, text = "z: ", fg="blue", font=("Helvetica", 14)).grid(column=4, row=2)
        self.maxzangleEntry = Entry(self.ParamFrame, width = 3)
        self.maxzangleEntry.insert(0, "0.5")
        self.maxzangleEntry.grid(column=5, row=2)
            # xyz message
        self.setAngleMessage = Label(self.ParamFrame, text = "", fg="red", font=("Helvetica", 12))
        self.setAngleMessage.grid(columnspan=4, column=2, row=3)

        # choose image width and height in generating positives
        self.width_Label = Label(self.ParamFrame, text = "Positive Image Width in Background: ", fg="blue", font=("Helvetica", 14)).grid(columnspan=4, column=0, row=4)
        self.width_Entry = Entry(self.ParamFrame, width = 5)
        self.width_Entry.insert(0, "20")
        self.width_Entry.grid(column=5, row=4)

        self.height_Label = Label(self.ParamFrame, text = "Positive Image Height in Background:", fg="blue", font=("Helvetica", 14)).grid(columnspan=4, column=0, row=5)
        self.height_Entry = Entry(self.ParamFrame, width = 5)
        self.height_Entry.insert(0, "20")
        self.height_Entry.grid(column=5, row=5)
        self.width_height_Message = Label(self.ParamFrame, text = "", fg="red", font=("Helvetica", 12))
        self.width_height_Message.grid(columnspan=4, column=1, row=6)

        # train number of stages
        self.trainStageLabel = Label(self.ParamFrame, text = "Train Stage Number:", fg="blue", font=("Helvetica", 14)).grid(columnspan=4, column=0, row=7)
        self.trainStageEntry = Entry(self.ParamFrame, width = 5)
        self.trainStageEntry.insert(0, "20")
        self.trainStageEntry.grid(column=5, row=7)
        self.trainStageEntryMessage = Label(self.ParamFrame, text = "", fg="red", font=("Helvetica", 12))
        self.trainStageEntryMessage.grid(columnspan=4, column=1, row=8)

        self._drawSpace()

        # submit button
        self.AcceptFrame = Frame(self.ParametersPanelFrame)
        self.AcceptFrame.pack()
        self.returnButton = Button(self.AcceptFrame, text = "Back", command=self._return).grid(column=0, row=0)
        self.gapLabel1 = Label(self.AcceptFrame, text = " "*5).grid(column=1, row=0)
        self.setDefaultButton = Button(self.AcceptFrame, text = "Reset", command=self._resetDefaultParameters).grid(column=2, row=0)
        self.gapLabel2 = Label(self.AcceptFrame, text = " "*5).grid(column=3, row=0)
        self.AcceptButton = Button(self.AcceptFrame, text = "Parameter Applied", command=self._submit).grid(column=4, row=0)

    def _drawHorizontalLine(self):
        self.canvas1 = Canvas(self.ParametersPanelFrame, width=400, height=20)
        self.canvas1.pack()
        self.seperateLine1 = self.canvas1.create_line(5, 10, 400, 10, fill="gray")

    def _drawSpace(self):
        Canvas(self.ParametersPanelFrame, width=400, height=10).pack()

    def _generateBackgroundTXTFile(self):
        with open('bg.txt', 'a') as f:
            for img in os.listdir(self.negativePath):
                line = self.negativePath + img + '\n'
                f.write(line)

    def _isValidParameters(self):
        self._updateModifiedParameters()
        lowerBound, angleUpperBound, widthHeightUpperBound = str(0), str(1), str(50)
        if len(os.listdir(self.negativePath)) < 1500:
            self.chooseImageMessage['fg'] = "red"
            self.chooseImageMessage['text'] = "< 1500 Images"
            return False
        if self.maxxangle == "" or self.maxxangle <= lowerBound or self.maxxangle >= angleUpperBound \
            or self.maxyangle == "" or self.maxyangle <= lowerBound or self.maxyangle >= angleUpperBound \
                or self.maxzangle == "" or self.maxzangle <= lowerBound or self.maxzangle >= angleUpperBound:
            self.setAngleMessage["text"] = "x, y, z must be between 0 and 1."
            return False
        if self.positiveImageWidth == "" or self.positiveImageWidth <= lowerBound or self.positiveImageWidth >= widthHeightUpperBound \
            or self.positiveImageHeight == "" or self.positiveImageHeight <= lowerBound or self.positiveImageHeight >= widthHeightUpperBound:
            self.width_height_Message['text'] = "Width and height must be less than 50"
            return False
        if self.numStages == "" or self.numStages <= lowerBound:
            self.trainStageEntryMessage['text'] = "Train Stage Number must be bigger than 1"
            return False
        return True

    def _submit(self):
        if not self._isValidParameters():
            return
        else:
            self.ParametersPanelFrame.pack_forget()
            self.appMain.appMainFrame.pack()
            self.appMain.setParamMessage["fg"] = "green"
            self.appMain.setParamMessage["text"] = "Parameters Applied"


    def _return(self):
        self._setDefaultValues()
        self._submit()


    def _set_max_x_y_z_angles(self, x, y, z):
        self.maxxangle = x
        self.maxyangle = y
        self.maxzangle = z

    def _updateModifiedParameters(self):
        self.maxxangle = self.maxxangleEntry.get()
        self.maxyangle = self.maxyangleEntry.get()
        self.maxzangle = self.maxzangleEntry.get()
        self.positiveImageWidth = self.width_Entry.get()
        self.positiveImageHeight = self.height_Entry.get()
        self.numStages = self.trainStageEntry.get()

    def _resetDefaultParameters(self):
        self._setDefaultValues()
        self._clearAllEntryLabels()
        self.maxxangleEntry.insert(0, "0.5")
        self.maxyangleEntry.insert(0, "0.5")
        self.maxzangleEntry.insert(0, "0.5")
        self.width_Entry.insert(0, "20")
        self.height_Entry.insert(0, "20")
        self.trainStageEntry.insert(0, "20")
        self._clearAllMessageLabels()

    def _clearAllEntryLabels(self):
        self.maxxangleEntry.delete(0, END)
        self.maxyangleEntry.delete(0, END)
        self.maxzangleEntry.delete(0, END)
        self.width_Entry.delete(0, END)
        self.height_Entry.delete(0, END)
        self.trainStageEntry.delete(0, END)

    def _clearAllMessageLabels(self):
        self.chooseImageMessage['text'] = ""
        self.setAngleMessage['text'] = ""
        self.width_height_Message['text'] = ""
        self.trainStageEntryMessage['text'] = ""

    def _chooseImage(self):
        self._clearAllMessageLabels()
        self.negativePath = filedialog.askdirectory()
        if self.negativePath == "" or self.negativePath in self._getForbiddenDirectoryAndFileSet():
            self._setDefaultNegativePath()
            return
        if len(os.listdir(self.negativePath)) < 1500:
            self.chooseImageMessage['fg'] = "red"
            self.chooseImageMessage['text'] = "< 1500 Images"
        else:
            self.chooseImageMessage['fg'] = "green"
            self.chooseImageMessage['text'] = "Directory Applied"
