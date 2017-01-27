
# Created by: Qingquan Zhao

from tkinter import *
import tkinter.filedialog as filedialog
import tkinter.messagebox
from PIL import Image, ImageTk
import os
import shutil
import platform
from src.ParameterPanel import Parameters
from src.ControlHandler import TrainImageHandler, TestHandler


class AppMain():

	def __init__(self, root):
		self.root = root
		self.root.minsize(width=450, height=450)
		self.root.resizable(width=False, height=False)
		self.initiateGUI()
		self.parameters = Parameters(self)
		self.imageToBeTrainedPath = None
		self.imageToBeTrainedFileName = None
		self.cascadeFilePath = None
		self.handler = None
		self.imageToBeDetectedPath = None

	def initiateGUI(self):

		self.appMainFrame = Frame(self.root)
		self.appMainFrame.pack()

		self._drawSpace()
		self.title = Label(self.appMainFrame, text = 'Item Recognizer', fg="red", font=("Helvetica", 26), anchor=CENTER)
		self.title.pack(side = TOP)

		self._drawHorizontalLine()

		self.trainFrame = Frame(self.appMainFrame)
		self.trainFrame.pack()
		self.trainSuperLabel = Label(self.trainFrame, text = "Train: ", fg="red", font=("Helvetica", 20)).grid(column = 0,row = 0)

		self.trainStepLabel1 = Label(self.trainFrame, text = "1.", fg="blue", font=("Helvetica", 16)).grid(column=1, row=0)
		self.chooseImageLabel = Label(self.trainFrame, text = "Choose an image (50x50)", fg="blue", font=("Helvetica", 16)).grid(column=2, row=0)
		self.chooseImageButton = Button(self.trainFrame, text = "Choose Image", command=self.chooseImage).grid(column=3, row=0)
		self.chooseImageMessage = Label(self.trainFrame, text = "", fg="red", font=("Helvetica", 12))
		self.chooseImageMessage.grid(columnspan=2, column=2, row=1)

		self.trainStepLabel2 = Label(self.trainFrame, text = "2.", fg="blue", font=("Helvetica", 16)).grid(column=1, row=2)
		self.setParamLabel = Label(self.trainFrame, text = "Set Parameters", fg="blue", font=("Helvetica", 16)).grid(column=2, row=2)
		self.setParamButton = Button(self.trainFrame, text = "Set Parameters", command=self._editParameters).grid(column=3, row=2)
		self.setParamMessage = Label(self.trainFrame, text = "", fg="red", font=("Helvetica", 12))
		self.setParamMessage.grid(columnspan=2, column=2, row=3)

		self.trainStepLabel3 = Label(self.trainFrame, text = "3.", fg="blue", font=("Helvetica", 16)).grid(column=1, row=4)
		self.startTrainLabel = Label(self.trainFrame, text = "Start Training", fg="blue", font=("Helvetica", 16)).grid(column=2, row=4)
		self.startTrainButton = Button(self.trainFrame, text = "Start Training", command=self.trainImage).grid(column=3, row=4)
		self.startTrainMessage = Label(self.trainFrame, text = "", fg="red", font=("Helvetica", 12))
		self.startTrainMessage.grid(columnspan=2, column=2, row=5)

		self._drawHorizontalLine()

		self.testFrame = Frame(self.appMainFrame)
		self.testFrame.pack()
		self.trainSuperLabel = Label(self.testFrame, text = "Test: ", fg="red", font=("Helvetica", 20)).grid(column = 0,row = 0)

		self.testStepLabel1 = Label(self.testFrame, text = "1.", fg="blue", font=("Helvetica", 16)).grid(column=1, row=0)
		self.chooseCascadeFileLabel = Label(self.testFrame, text = "Choose Cascade File", fg="blue", font=("Helvetica", 16)).grid(column=2, row=0)
		self.chooseCascadeFileButton = Button(self.testFrame, text = "Cascade File", command=self.chooseCascadeFile).grid(column=3, row=0)
		self.chooseCascadeFileMessage = Label(self.testFrame, text = "", fg="red", font=("Helvetica", 12))
		self.chooseCascadeFileMessage.grid(columnspan=2, column=2, row=1)

		self.testStepLabel2 = Label(self.testFrame, text = "2.", fg="blue", font=("Helvetica", 16)).grid(column=1, row=2)
		self.videoDetectionLabel = Label(self.testFrame, text = "Video Detection", fg="blue", font=("Helvetica", 16)).grid(column=2, row=2)
		self.videoDetectionButton = Button(self.testFrame, text = "Video Test", command=self.testVideo).grid(column=3, row=2)
		self.videoDetectionMessage = Label(self.testFrame, text = "", fg="red", font=("Helvetica", 12))
		self.videoDetectionMessage.grid(columnspan=2, column=2, row=3)

		self.testStepLabel3 = Label(self.testFrame, text = "3.", fg="blue", font=("Helvetica", 16)).grid(column=1, row=4)
		self.imageDetectionLabel = Label(self.testFrame, text = "Image Detection", fg="blue", font=("Helvetica", 16)).grid(column=2, row=4)
		self.imageDetectionButton = Button(self.testFrame, text = "Image Test", command=self.testImage).grid(column=3, row=4)
		self.imageDetectionMessage = Label(self.testFrame, text = "", fg="red", font=("Helvetica", 12))
		self.imageDetectionMessage.grid(columnspan=2, column=2, row=5)

	def _drawHorizontalLine(self):
		self.canvas1 = Canvas(self.appMainFrame, width=400, height=20)
		self.canvas1.pack()
		self.seperateLine1 = self.canvas1.create_line(5, 10, 400, 10, fill="gray")

	def _drawSpace(self):
		Canvas(self.appMainFrame, width=400, height=10).pack()

	def _editParameters(self):
		self.appMainFrame.pack_forget()
		self.parameters.initiateGUI()

	def clearAllMessageLabel(self):
		self.chooseImageMessage['text'] = ""
		self.setParamMessage['text'] = ""
		self.startTrainMessage['text'] = ""
		self.chooseCascadeFileMessage['text'] = ""
		self.videoDetectionMessage['text'] = ""
		self.imageDetectionMessage['text'] = ""

	def chooseImage(self):
		self.clearAllMessageLabel()
		fileChosen = filedialog.askopenfile()
		try:
			fileNameChosen = fileChosen.name
		except Exception:
			self.imageToBeTrainedPath = ""
			return
		if not fileNameChosen.endswith(".png"):
			self.chooseImageMessage["fg"] = "red"
			self.chooseImageMessage["text"] = "Only .png file is allowed"
			return
		im = Image.open(fileNameChosen)

		if im.size[0] == 50 and im.size[1] == 50:
			self.imageToBeTrainedPath = fileNameChosen
			self.chooseImageMessage["fg"] = "green"
			self.chooseImageMessage["text"] = "Image is Valid, click Start Training button to train"
		else:
			self.chooseImageMessage["fg"] = "red"
			self.chooseImageMessage["text"] = "Image size need to be 50X50"
		return

	def trainImage(self):
		self.clearAllMessageLabel()
		if self.imageToBeTrainedPath == None:
			self.startTrainMessage["fg"] = "red"
			self.startTrainMessage["text"] = "No Image was chosen, please choose a target image."
			return
		if not os.path.exists(self.parameters.negativePath) or not os.path.exists(self.parameters.bgTXT):
			self.startTrainMessage["fg"] = "red"
			self.startTrainMessage["text"] = "Background Image Library is missing!"
		else:
			self._cleanOldFiles()
			self._trainValidImage()
			self._setCascadeFilePath(self._getDefaultCascadeFile())

	def _getDefaultCascadeFile(self):
		if str(platform.system()) == 'darwin':
			return "data\\cascade.xml"
		else:
			return "data/cascade.xml"

	def _cleanOldFiles(self):
		required_dirs = [self.parameters.data, self.parameters.info]
		required_files = [self.parameters.positiveVec]
		for d in required_dirs:
			if os.path.exists(d):
				shutil.rmtree(d)
		for f in required_files:
			if os.path.exists(f):
				os.remove(f)

	def _trainValidImage(self):
		answer = tkinter.messagebox.askquestion('Start Training', 'Are you sure you want to start training? It might take a while.')
		if answer == "no":
			return
		self.startTrainMessage["fg"] = "green"
		self.startTrainMessage["text"] = "Training.... \nThis might take a while. \nCheck console to see if it is finished."
		self.imageToBeTrainedFileName = self.imageToBeTrainedPath.split("/")[-1]
		shutil.copyfile(self.imageToBeTrainedPath, self.imageToBeTrainedFileName)
		TrainImageHandler(self).trainCascade()
		self.startTrainMessage["text"] = "Train Finished !"
		os.remove(self.imageToBeTrainedFileName)
		self._applyCascadeFile(self._getDefaultCascadeFile())

	def _applyCascadeFile(self, path):
		self.handler = TestHandler(self)
		self._setCascadeFilePath(path)
		self.chooseCascadeFileMessage["fg"] = "green"
		self.chooseCascadeFileMessage["text"] = "Cascade File Applied"

	def chooseCascadeFile(self):
		self.clearAllMessageLabel()
		fileChosen = filedialog.askopenfile()
		try:
			fileNameChosen = fileChosen.name
		except Exception:
			return
		if not fileNameChosen.endswith(".xml"):
			self.chooseCascadeFileMessage["fg"] = "red"
			self.chooseCascadeFileMessage["text"] = "Cascade Files Must Be XML File."
			return
		self._applyCascadeFile(fileNameChosen)

	def _setCascadeFilePath(self, path):
		self.cascadeFilePath = path

	def testVideo(self):
		self.clearAllMessageLabel()
		if self.handler == None:
			self.videoDetectionMessage["fg"] = "red"
			self.videoDetectionMessage["text"] = "Missing Cascade File"
			return
		try:
			self.handler.testVideo()
		except Exception:
			self.videoDetectionMessage["fg"] = "red"
			self.videoDetectionMessage["text"] = "Invalid Cascade File"

	def testImage(self):
		self.clearAllMessageLabel()
		if self.imageToBeTrainedPath == None:
			self.imageDetectionMessage["fg"] = "red"
			self.imageDetectionMessage["text"] = "Source Image Missing"
			self.chooseImageMessage["fg"] = "red"
			self.chooseImageMessage['text'] = "Please Choose An Image"
			return
		if self.cascadeFilePath == None:
			self.imageDetectionMessage["fg"] = "red"
			self.imageDetectionMessage["text"] = "Cascade File Missing"
			self.chooseCascadeFileMessage["fg"] = "red"
			self.chooseCascadeFileMessage['text'] = "Please Choose A Cascade File"
			return
		# chosoe image file to be detected
		fileChosen = filedialog.askopenfile()
		try:
			fileNameChosen = fileChosen.name
		except Exception:
			self.imageToBeDetectedPath = ""
			return
		if not fileNameChosen.endswith(".png"):
			self.imageDetectionMessage["fg"] = "red"
			self.imageDetectionMessage["text"] = "Only .png file is allowed"
			return
		self.imageToBeDetectedPath = fileNameChosen

		# check if cascade file is missing or invalid
		if self.handler == None:

			return
		try:
			self.handler.testImage(self.imageToBeDetectedPath)
		except Exception:
			self.imageDetectionMessage["fg"] = "red"
			self.imageDetectionMessage["text"] = "Invalid Cascade File"

