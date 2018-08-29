from tkinter import *
from tkinter import ttk
from Model import recover

from View import recoveryFrame
import os.path

class reCoveryInterface:
	def __init__(self):
		self.gcodeVar=StringVar()
		self.gcodeVar.set("")
		self.restartBool=BooleanVar()
		self.restartBool.set(True)
		self.heightVar=DoubleVar()
		self.heightVar.set(0)
		self.restartheightindex= IntVar()
		self.restartheightindex.set(0)

	def initialize(self, model, view):
		view.summon(model,self) #Creates Interface


'''
	def process_gcode(self,obj,event=None):
		if(len(self.gcodeVar.get())==0):
			self.master.output.insert(END,">>> Please insert a valid gcode file!\n")
			self.master.output.see("end")
		if(self.heightVar.get()==0):
			self.master.output.insert(END,">>> Invalid height measurement.\n")
			self.master.output.see("end")
		else:
			obj.filename=self.gcodeVar.get()
			obj.restart=self.restartBool.get()
			obj.layerheight=self.heightVar.get()
			fail= obj.generate_resume_heights()
			if(fail):
				self.master.output.insert(END,">>> Invalid Gcode file.\n")
				self.master.output.see("end")

			if(len(obj.resumeheights)==0):
				self.master.output.insert(END,">>> Invalid height measurement.\n")
				self.master.output.see("end")
			else:
				print(self.restartheightindex.get())
				print(obj.resumeheights)
				self.master.value1.delete(1.0,END)
				self.master.value2.delete(1.0,END)
				self.master.value1.insert(END,obj.resumeheights[0])
				self.master.value2.insert(END,obj.resumeheights[1])
				self.master.output.insert(END,">>> Gcode processed! Please select a layer height and press Generate reCovery File.\n")
				self.master.output.see("end")

	def generate_recovery_file(self,obj):
		obj.generate_recovery_file((self.restartheightindex.get()-1))
		self.master.output.insert(END,">>> reCovery file created! Run the follow gcode in machine: " + obj.newfilename+"\n")

	def reset(self,obj,event=None):
		obj.filename=""
		self.gcodeVar.set("")
		self.restartBool.set(True)
		self.heightVar.set(0)
		self.restartheightindex.set(0)
		self.master.value1.delete(1.0,END)
		self.master.value2.delete(1.0,END)
		obj.completed = False

	def summon(self, obj):
		logo_and_selection_frame = Frame(self.master.root)
		logo_and_selection_frame.grid(row=0,column=0)
		# <----- Re3D Logo ----->
		logo = Frame(logo_and_selection_frame)
		logo.grid(row=0,column=0,padx=5,pady=5)

		re3D = PhotoImage(file=self.imagename)
		logolabel=Label(logo,image=re3D)
		logolabel.grid(row=0,column=0, padx=5,pady=5)
		bylabel = Label(logo,text="by plloppii @ re3D")
		bylabel.grid(row=1,column=0)

		# <----- Master Selection Frame ----->
		selections = Frame(logo_and_selection_frame)
		selections.grid(row=0,column=1,padx=5,pady=5)

		# <----- Selection Part 1 ----->
		selection1 = Frame(selections)
		selection1.grid(row=0,column=0,sticky=W)
		intro = self.master.createlabel(selection1, "Welcome to re:3D's gcode reCovery program.",0,0,W,5,5)

		gcodelabel= self.master.createlabel(selection1,"Please enter your gcode file: ",1,0,W,3,3)
		self.master.gcodeentry = self.master.createentry(selection1, self.gcodeVar, 10, 1,1,E,3,3)

		heightlabel = self.master.createlabel(selection1, "What is the approximate height measurement of the failed print? (in mm) : ",2,0,W,3,3)
		self.master.heightentry = self.master.createentry(selection1,self.heightVar, 10,2,1,E,3,3)

		restartlabel = self.master.createlabel(selection1,"Did your printer reset? (ie. Power Outtage) : ",3,0,W,3,3)
		yesradio = self.master.createradio(selection1,"Yes",1,self.restartBool,3,1,E,3,0)
		noradio = self.master.createradio(selection1,"No",0,self.restartBool,4,1,E,3,0)

		# <----- Process Gcode button ----->
		button= Frame (selections)
		button.grid(row=5,column=0)

		processbutton = self.master.createbutton(button,"Process Gcode",0,0,E,3,3)
		processbutton.bind("<Button-1>",lambda event:self.process_gcode(obj))
		div = Frame(selections, height = 1, width =500, background="black")
		div.grid(row=6,column=0, pady= 10)

		# <----- Choose between two heights ----->
		chooseframe = Frame(selections)
		chooseframe.grid(row=7,column=0, sticky=W)
		chooseheight = self.master.createlabel(chooseframe,"I found two layer heights, please choose which one to resume on:        ",0,0,W,3,3)
		self.master.value1= self.master.createtext(chooseframe, 7, 1, 0,1,E,3,0)
		self.master.value2= self.master.createtext(chooseframe,7,1,1,1,E,3,0)

		value = Radiobutton(chooseframe, value = 0, variable = self.restartheightindex)
		value1radio	= Radiobutton(chooseframe,value=1, variable = self.restartheightindex)
		value1radio.grid(row=0,column=2,sticky=E)
		value2radio = Radiobutton(chooseframe,value=2, variable = self.restartheightindex)
		value2radio.grid(row=1,column=2,sticky=E)

		# <----- Generate and Reset Buttons ----->
		button1 = Frame(selections)
		button1.grid(row=8,column=0)
		generatebutton = self.master.createbutton(button1,"Generate reCovery File",0,0,E,3,3)
		generatebutton.bind("<Button-1>",lambda event: self.generate_recovery_file(obj))
		resetbutton = self.master.createbutton(button1,"Reset",0,1,W,3,3)
		resetbutton.bind("<Button-1>",lambda event: self.reset(obj))

		# <----- Console Output ----->
		outputframe = Frame(self.master.root)
		outputframe.grid(row=1,column=0,sticky="S")
		self.master.output = self.master.createtext(outputframe,80,7,0,0,S,3,3)
		scrollbar = Scrollbar(outputframe,command =self.master.output.yview )
		scrollbar.grid(row=0,column=1,sticky="nsew")

		self.master.output.config(yscrollcommand=scrollbar.set,wrap=WORD)
		self.master.root.title("re:Covery - re:3D gcode reCovery")
		self.master.root.mainloop()
'''
if __name__ =='__main__':
	model = recover() #Model Instance
	view = recoveryFrame("re3D.png") #Interface Instance

	controller= reCoveryInterface() 


	controller.initialize(model,view)


