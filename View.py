from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from myimage import *

class recoveryFrame:
	def __init__(self, imagename):
		self.root= Tk()
		self.imagename = imagename
		self.value1 = None
		self.value2 = None
		self.gcodeentry = None
		self.heightentry = None
		self.output = None
		self.filebutton = None


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

	def reset(self,event=None):
		self.value1.delete(1.0,END)
		self.value2.delete(1.0,END)
		self.filebutton.config(relief = RAISED)

	def requestfile(self):
		self.root.fileName = filedialog.askopenfilename(filetypes = (("Gcode files","*.gcode"),("all files","*.*")))

	def summon(self, model,controller):
		logo_and_selection_frame = Frame(self.root)
		logo_and_selection_frame.grid(row=0,column=0)
		# <----- Re3D Logo ----->
		logo = Frame(logo_and_selection_frame)
		logo.grid(row=0,column=0,padx=5,pady=5)

		pic = imageString
		render = PhotoImage(data=pic)
		#re3D = PhotoImage(file=self.imagename)
		logolabel=Label(logo,image=render)
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
		#self.gcodeentry = self.createentry(selection1, controller.gcodeVar, 10, 1,1,E,3,3) 
		self.filebutton = self.createbutton(selection1,"...",1,1,E,3,3)
		self.filebutton.bind("<Button-1>", lambda event: controller.filebuttonpressed())
		#root.fileName = filedialog.askopenfilename( filetypes = ( "Gcode","*.gcode" ) )
		#controller.gcodeVar = tkFileDialog.askopenfilename(initialdir = "/")

		heightlabel = self.createlabel(selection1, "What is the approximate height measurement of the failed print? (mm) : ",2,0,W,3,3)
		self.heightentry = self.createentry(selection1,controller.heightVar, 10,2,1,E,3,3) 

		restartlabel = self.createlabel(selection1,"Did your printer reset? (ie. Power Outtage) : ",3,0,W,3,3)
		unselectedradio = Radiobutton(selection1, value = -1, variable=controller.restartBool)
		yesradio = self.createradio(selection1,"Yes",1,controller.restartBool,3,1,E,3,0) 
		noradio = self.createradio(selection1,"No",0,controller.restartBool,4,1,E,3,0)

		# <----- Process Gcode button ----->
		button= Frame (selections)
		button.grid(row=5,column=0)

		processbutton = self.createbutton(button,"Process Gcode",0,0,E,3,3)
		processbutton.bind("<Button-1>",lambda event:controller.processbuttonpressed()) #X Inputing Model Instance
		div = Frame(selections, height = 1, width =500, background="black")
		div.grid(row=6,column=0, pady= 10)

		# <----- Choose between two heights ----->
		chooseframe = Frame(selections)
		chooseframe.grid(row=7,column=0, sticky=W)
		chooseheight = self.createlabel(chooseframe,"I found two layer heights, please choose which one to resume on:        ",0,0,W,3,3)
		self.value1= self.createtext(chooseframe, 7, 1, 0,1,E,3,0)
		self.value2= self.createtext(chooseframe,7,1,1,1,E,3,0)

		value = Radiobutton(chooseframe, value = -1, variable = controller.restartheightindex)
		value1radio	= Radiobutton(chooseframe,value=0, variable = controller.restartheightindex)
		value1radio.grid(row=0,column=2,sticky=E)
		value2radio = Radiobutton(chooseframe,value=1, variable = controller.restartheightindex)
		value2radio.grid(row=1,column=2,sticky=E)

		# <----- Generate and Reset Buttons ----->
		button1 = Frame(selections)
		button1.grid(row=8,column=0)
		generatebutton = self.createbutton(button1,"Generate reCovery File",0,0,E,3,3)
		generatebutton.bind("<Button-1>",lambda event: controller.generatebuttonpressed()) #X Inputting Model Instance
		resetbutton = self.createbutton(button1,"Reset",0,1,W,3,3)
		resetbutton.bind("<Button-1>",lambda event: controller.resetbuttonpressed()) #X Inputting Model Instance

		# <----- Console Output ----->
		outputframe = Frame(self.root)
		outputframe.grid(row=1,column=0,sticky="S")
		self.output = self.createtext(outputframe,80,7,0,0,S,3,3)
		scrollbar = Scrollbar(outputframe,command =self.output.yview ) 
		scrollbar.grid(row=0,column=1,sticky="nsew")

		self.output.config(yscrollcommand=scrollbar.set,wrap=WORD)

		# <----- Title and Mainloop ----->
		self.root.title("re:Covery - re:3D gcode reCovery")
		self.root.mainloop()
