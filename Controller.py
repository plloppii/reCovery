from tkinter import *
from tkinter import ttk

#import Model
#import View

from Model import recover
from View import recoveryFrame

from os.path import isfile

class reCoveryInterface:
	def __init__(self,model,view):
		self.model= model
		self.view= view
		self.gcodeVar=StringVar()
		self.gcodeVar.set("")
		self.restartBool=IntVar()
		self.restartBool.set(-1)
		self.heightVar=DoubleVar()
		self.heightVar.set(0)
		self.restartheightindex= IntVar()
		self.restartheightindex.set(-1)

	def initialize(self):
		self.view.summon(self.model,self) #Creates Interface

	def processbuttonpressed(self):
		if(self.check(1)):
			self.model.restart = self.restartBool.get()
			self.model.layerheight = self.heightVar.get()
			self.model.generate_resume_heights()
			if(self.check(2)):
				self.updatelayerheights()

	def updatelayerheights(self):
		self.view.value1.delete(1.0,END)
		self.view.value2.delete(1.0,END)
		self.view.value1.insert(END,self.model.resumeheights[0])
		self.view.value2.insert(END,self.model.resumeheights[1])
		self.displayinconsole(">>> Gcode processed! Please select a layer height and press Generate reCovery File")

	def check(self,case):
		if(case == 1):
			if (not(isfile(self.model.dir + self.model.filename))):
				self.displayinconsole(">>> Please enter a valid gcode file")
				return False
			if (self.heightVar.get() == 0 or self.heightVar.get() == ""):
				self.displayinconsole(">>> Please enter a valid height measurement")
				return False
			if (self.restartBool.get() == -1):
				self.displayinconsole(">>> Please select if your printer reset")
				return False
			return True
		if(case == 2):
			if (len(self.model.resumeheights) == 0):
				self.displayinconsole(">>> Height measurement is out of bounds/ invalid")
				return False
			return True
		if(case == 3):
			if(self.restartheightindex.get() == -1):
				self.displayinconsole(">>> Please select a valid layer height to resume on")
				return False
			return True

	def generatebuttonpressed(self):
		if(self.check(1) and self.check(2) and self.check(3)):
			self.model.generate_recovery_file(controller.restartheightindex.get())
			self.displayinconsole(">>> reCovery file created! Run the follow gcode in machine: " + self.model.newfilename)

	def resetbuttonpressed(self):
		self.reset()
		self.view.reset()
		self.model.reset()

	def reset(self):
		self.gcodeVar.set("")
		self.restartBool.set(-1)
		self.heightVar.set(0)
		self.restartheightindex.set(-1)

	def filebuttonpressed(self):
		self.view.requestfile()
		self.processfile()

	def processfile(self):
		dirr= self.view.root.fileName
		name = ""
		while (dirr[-1] != "/"):
			name = dirr[-1]+name
			dirr = dirr[:-1]
		self.model.filename = name
		self.model.dir = dirr
		print(self.model.filename)
		print(self.model.dir)

	def displayinconsole(self,string):
		self.view.output.insert(END,(string+"\n"))
		self.view.output.see("end")

'''
				self.master.output.insert(END,">>> Invalid height measurement.\n")
				self.master.output.see("end")
'''
if __name__ =='__main__':
	model = recover() #Model Instance
	view = recoveryFrame("re3D.png") #Interface Instance
	controller= reCoveryInterface(model,view) 


	controller.initialize()


