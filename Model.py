import os.path
from tkinter import BOTH, END, LEFT

class recover:
	def __init__(self):
		self.filename= ""
		self.newfilename=""
		self.restart= False
		self.layerheight= 0
		self.resumeheights=[] #Stores the two heights that is below and above the user's input height
		self.start= [0,0]
		self.failedfile = {}
		self.completed = False

	def reset(self):
		self.filename = ""
		self.completed = False
		self.restart = False
		self.newfilename = ""
		self.layerheight = 0
		self.resumeheights = []
		self.start= [0,0]
		self.failedfile = {}

	def generate_resume_heights(self):
		startinggcode = ["M104", "M190", "M140", "M109", "T0", "M900", "M605", "M92", "M220", "M221","G28"]
		
		lineindex=0 #variable for the current lineindex
		height=0 #variable for the current zheight
		lastheight=0 #variable for the last zheight  
		failedfile= {} #Stores file into a hashmap
		self.start= [0,0] #Stores the two lineindex for the resumeheights

		nfilename = self.filename.replace(".gcode","")
		self.newfilename = (nfilename+"_reCovered.gcode")
		self.resumeheights=[]

		failed= open(self.filename, "r")
		recovered = open(self.newfilename,"w")
		for line in failed:
			if ("; process" in line) or (line[0] == ";"): #ignore process lines and comments
				pass
			else:
				if "Z=" in line:
					x = "0"
					i=0
					for char in line:
						if char == "=":
							x += line[i+1:-1]
						i+=1
					height = float(x)
					if(self.start[1]==0):
						lastindex=self.start[0]
						self.start[0]=lineindex
					#print(height)
				if (self.layerheight < height) and (len(self.resumeheights)==0):
					self.start[0]=lastindex
					self.start[1]=lineindex
					self.resumeheights.append(lastheight)
					self.resumeheights.append(height)
				lastheight = height

				for gcode in startinggcode:
					if gcode in line:
						if (gcode == "M221") & (lineindex>250):
							pass
						elif "G28" in line:
							if self.restart==1:
								recovered.write(line)
							else:
								recovered.write("G28 X Y \n")
						else:
							recovered.write(line)
			self.failedfile[lineindex]=line
			lineindex+=1
		failed.close()
		recovered.close()


	def generate_recovery_file(self,index):
		#resumeline= int(input("I found two layer heights around that value: %.3f(0) and %.3f(1). Which one would you like to continue on? : "%(resumeheights[0],resumeheights[1])))
		recovered = open(self.newfilename,"a")
		i=self.start[index]
		recovered.write("\nG1 Z%.3f\n" % (self.resumeheights[index]))
		while(i<len(self.failedfile)):
			recovered.write(self.failedfile[i])
			i+=1
		self.completed = True
		#print("reCovery file created! Run the follow gcode in machine: " + self.newfilename)
		recovered.close()

