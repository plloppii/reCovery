from tkinter import *
from tkinter import ttk

class recoveryFrame:
	def __init__(self):
		self.root= Tk()
		self.value1 = None
		self.value2 = None
		self.gcodeentry = None
		self.heightentry = None
		self.output = None


	def creategrid(self,widget, row, column, sticky, padx, pady):
		widget.grid(row = row, column = column, sticky= sticky, padx= padx, pady= pady)

	def createtext(self, master,width, height , row, column, sticky, padx, pady):
		widget = Text(master, width= width, height = height)
		self.creategrid(widget, row, column, sticky, padx, pady)
		return widget
	def createlabel(self,master,text, row,column,sticky,padx,pady):
		widget= Label(master,text= text)
		self.creategrid(widget, row, column, sticky, padx, pady)
		return widget
	def createentry(self, master, textvariable, width, row, column, sticky, padx, pady):
		widget = Entry(master,textvariable=textvariable, width=width)
		self.creategrid(widget, row, column, sticky, padx, pady)
		return widget
	def createradio(self,master,text,value,variable,row,column,sticky,padx,pady):
		widget = Radiobutton(master, text = text, value= value, variable= variable)
		self.creategrid(widget, row, column, sticky, padx, pady)
		return widget
	def createbutton(self,master,text,row,column,sticky,padx,pady):
		widget = Button(master,text=text)
		self.creategrid(widget, row, column, sticky, padx, pady)
		return widget

	def summon(self, obj):
		logo_and_selection_frame = Frame(self.root)
		logo_and_selection_frame.grid(row=0,column=0)
		# <----- Re3D Logo ----->
		logo = Frame(logo_and_selection_frame)
		logo.grid(row=0,column=0,padx=5,pady=5)

		re3D = PhotoImage(file=self.imagename) #X
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
		intro = self.createlabel(selection1, "Welcome to re:3D's gcode reCovery program.",0,0,W,5,5)

		gcodelabel= self.createlabel(selection1,"Please enter your gcode file: ",1,0,W,3,3)
		self.master.gcodeentry = self.createentry(selection1, self.gcodeVar, 10, 1,1,E,3,3) #X

		heightlabel = self.createlabel(selection1, "What is the approximate height measurement of the failed print? (in mm) : ",2,0,W,3,3)
		self.heightentry = self.createentry(selection1,self.heightVar, 10,2,1,E,3,3) #X

		restartlabel = self.createlabel(selection1,"Did your printer reset? (ie. Power Outtage) : ",3,0,W,3,3)
		yesradio = self.createradio(selection1,"Yes",1,self.restartBool,3,1,E,3,0) #X
		noradio = self.createradio(selection1,"No",0,self.restartBool,4,1,E,3,0) #X

		# <----- Process Gcode button ----->
		button= Frame (selections)
		button.grid(row=5,column=0)

		processbutton = self.createbutton(button,"Process Gcode",0,0,E,3,3)
		processbutton.bind("<Button-1>",lambda event:self.process_gcode(obj)) #X Inputing Model Instance
		div = Frame(selections, height = 1, width =500, background="black")
		div.grid(row=6,column=0, pady= 10)

		# <----- Choose between two heights ----->
		chooseframe = Frame(selections)
		chooseframe.grid(row=7,column=0, sticky=W)
		chooseheight = self.createlabel(chooseframe,"I found two layer heights, please choose which one to resume on:        ",0,0,W,3,3)
		self.master.value1= self.createtext(chooseframe, 7, 1, 0,1,E,3,0)
		self.master.value2= self.createtext(chooseframe,7,1,1,1,E,3,0)

		value = Radiobutton(chooseframe, value = 0, variable = self.restartheightindex) #X
		value1radio	= Radiobutton(chooseframe,value=1, variable = self.restartheightindex) #X
		value1radio.grid(row=0,column=2,sticky=E)
		value2radio = Radiobutton(chooseframe,value=2, variable = self.restartheightindex) #X
		value2radio.grid(row=1,column=2,sticky=E)

		# <----- Generate and Reset Buttons ----->
		button1 = Frame(selections)
		button1.grid(row=8,column=0)
		generatebutton = self.createbutton(button1,"Generate reCovery File",0,0,E,3,3)
		generatebutton.bind("<Button-1>",lambda event: self.generate_recovery_file(obj)) #X Inputting Model Instance
		resetbutton = self.createbutton(button1,"Reset",0,1,W,3,3)
		resetbutton.bind("<Button-1>",lambda event: self.reset(obj)) #X Inputting Model Instance

		# <----- Console Output ----->
		outputframe = Frame(self.root)
		outputframe.grid(row=1,column=0,sticky="S")
		self.output = self.createtext(outputframe,80,7,0,0,S,3,3)
		scrollbar = Scrollbar(outputframe,command =self.output.yview ) 
		scrollbar.grid(row=0,column=1,sticky="nsew")

		self.output.config(yscrollcommand=scrollbar.set,wrap=WORD)
		self.root.title("re:Covery - re:3D gcode reCovery")
		self.root.mainloop()
