# access command line arguments
import os 
import time
import wmi 

from PySide2 import QtGui
from PySide2.QtWidgets import QWidget, QLabel, QFrame, QProgressBar, QVBoxLayout
from PySide2.QtCore import Qt, QTimer
from config import Config

from setup import SetupWindow
from user_interfaces import verify

# STYLESHEET FILE
from stylesheet import STYLES

from user_interfaces.home_window import BaseGuiWindow


class SplashScreen(QWidget):
	def __init__(self):
		super().__init__()
		self.setFixedSize(700, 350)
		self.setWindowFlag(Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.counter = 0
		self.n = 100 
		self.initUI()
		self.timer = QTimer()
		self.timer.timeout.connect(self.loading)
		self.timer.start(100)
		self.setStyleSheet(STYLES.splash)
		self.frame.setStyleSheet("background-color: rgb(33, 37, 43);") 
		self.frame.setStyleSheet("background-image: url(\':/tab_icons/home-image.png\');")
		self.setStyleSheet("border-radius: 15px; border: 3px solid grey; ")

	def initUI(self):
		# layout to display splash scrren frame
		layout = QVBoxLayout()
		self.setLayout(layout)
		# splash screen frame
		self.frame = QFrame()
		self.frame.setObjectName("frame")
		layout.addWidget(self.frame)
		# splash screen title
		self.title_label = QLabel(self.frame)
		self.title_label.setObjectName('title_label')
		self.title_label.resize(690, 120)
		self.title_label.move(0, 5) # x, y
		self.title_label.setText(Config.APP_NAME)
		self.title_label.setFont(QtGui.QFont("Montserrat Alternates"))
		self.title_label.setAlignment(Qt.AlignCenter)
		# splash screen pogressbar
		self.progressBar = QProgressBar(self.frame)
		self.progressBar.resize(self.width() - 200 - 10, 50)
		self.progressBar.move(100, 180) # self.description_label.y()+130
		self.progressBar.setAlignment(Qt.AlignCenter)
		self.progressBar.setFormat('%p%')
		self.progressBar.setTextVisible(True)
		self.progressBar.setRange(0, self.n)
		self.progressBar.setValue(20)
		self.progressBar.setStyleSheet("background-color: #4D77FF;")

	def loading(self):
		# set progressbar value
		self.progressBar.setValue(self.counter)
		# stop progress if counter
		# is greater than n and
		# display main window app
		if self.counter >= self.n:
			self.timer.stop()
			self.close()
			time.sleep(1)
			self.main_app = self.verify_license()
			self.main_app.show()
		self.counter += 2.75

	def verify_license(self):
		DIR_PATH = os.getenv('LOCALAPPDATA')
		FILE = "yagamie.key"
		if os.path.isfile(os.path.join(DIR_PATH, FILE)):
			with open(os.path.join(DIR_PATH, FILE), "r") as f:
				key = f.readline()
			chars = key.split("+=")
			key_id = chars[0]
			key_address = chars[1]
			blob = self.get_hardware_id()
			
			if (blob == key_id) and verify(key_address):
				return BaseGuiWindow()
			else:
				return SetupWindow()
		else:
			return SetupWindow()
	
	def get_hardware_id(self):
		c = wmi.WMI()
		hardware_id = []
		for item in c.Win32_PhysicalMedia():
			if item.SerialNumber != None:
				hardware_id.append(item.SerialNumber)
		return hardware_id[0].strip(" ")
