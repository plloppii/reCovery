import os.path
from tkinter import BOTH, END, LEFT

class recover:
	def __init__(self):
		self.filename= "" #User Input
		self.dir = ""
		self.newfilename= ""
		self.newlocation = ""
		self.restart= False #User Input
		self.layerheight= 0 #User Input
		self.resumeheights=[] #Stores the two heights that is below and above the user's input height
		self.start= [0,0]
		self.failedfile = {}
		#self.startinggcode = ["M104", "M190", "M140", "M109", "T0", "M900", "M605", "M92", "M220", "M221"]
		self.startinggcodeextracted = False
		self.lastheight = 0
		self.lineindex = 0
		self.lastindex = 0
		self.g28seen = False

	def reset(self):
		self.filename = ""
		self.restart = False
		self.newfilename = ""
		self.layerheight = 0 
		self.resumeheights = []
		self.start= [0,0]
		self.failedfile = {}
		self.startinggcodeextracted = False
		self.lastheight = 0
		self.lineindex = 0
		self.lastindex = 0
		self.g28seen = False

	def generate_resume_heights(self):		
		self.lineindex=0 #variable for the current lineindex
		lastheight=0 #variable for the last zheight  
		self.start= [0,0] #Stores the two lineindex for the resumeheights
		self.g28seen = False
		
		nfilename = self.filename.replace(".gcode","")
		self.newfilename = (nfilename+"_reCovered.gcode")
		self.resumeheights=[]

		self.newlocation = self.dir + self.newfilename
		failed= open(self.dir + self.filename, "r")
		recovered = open(self.newlocation,"w")
		self.startinggcodeextracted = False


		recovered.write("Recovery File Generated by re:3D's reCovery Application \n")
		recovered.write("Visit re:3D.org for more information \n")
		for line in failed:
			if(not(self.startinggcodeextracted)):
				self.check(line,recovered)
			if(self.startinggcodeextracted):
				self.checklayer(line)
			self.failedfile[self.lineindex] = line
			self.lineindex+=1

		failed.close()
		recovered.close()

	def checklayer(self,line):
		code = line[0:2]
		height = 0
		if (("G0" == code or "G1"== code) and ("Z" in line)):
			i = line.find("Z")
			l = len(line)-1
			z=""
			while(i+1<=l and line[i+1] != " "):
				z += line[i+1]
				i+=1
			height = float(z)
			if(self.start[1]==0): #Case where it hits the first height
				self.lastindex= self.start[0]
				self.start[0] = self.lineindex
		if (self.layerheight < height) and (len(self.resumeheights)==0):
			self.start[0] = self.lastindex
			self.start[1] = self.lineindex
			self.resumeheights.append(self.lastheight)
			self.resumeheights.append(height)
		if (height > 0):
			self.lastheight = height


	def check(self,line,recovered):
		if(line[0] == ";"):
			recovered.write(line)
		elif(self.checkG28(line)): #Returns true if line is G28 and a G28 gcode line is not already in the recovery file.
			if (self.restart == 1):
				recovered.write("G28 \n")
				self.g28seen = True
			elif (self.restart == 0):
				recovered.write("G28 X Y \n")
				self.g28seen = True
		elif(self.linecontainZ(line)):
			recovered.write(line)
		if(self.checkextracted(line)):
			self.startinggcodeextracted = True


	def checkG28(self,line):
		if("G28" in line and not self.g28seen):
			#for key in self.failedfile:
			#	if "G28" in self.failedfile[key]:
			#		return False
			return True
		return False

	def linecontainZ(self,line):
		code = line[0:2]
		if(("G0" in line or "G1" in line) and "Z" in line):
			return False
		if("G28" in line and self.g28seen):
			return False
		if (("G0" == code or "G1"== code) and ("X" in line or "Y" in line)):
			return False
		return True
	def checkextracted(self,line):
		code = line[0:2]
		if (("G0" == code or "G1"== code) and ("X" in line or "Y" in line)):
			return True
		return False

	def generate_recovery_file(self,index):
		#resumeline= int(input("I found two layer heights around that value: %.3f(0) and %.3f(1). Which one would you like to continue on? : "%(resumeheights[0],resumeheights[1])))
		recovered = open(self.newlocation,"a")
		i=self.start[index]
		recovered.write("\nG1 Z%.3f\n" % (self.resumeheights[index]))
		while(i<len(self.failedfile)):
			recovered.write(self.failedfile[i])
			i+=1
		#print("reCovery file created! Run the follow gcode in machine: " + self.newfilename)
		recovered.close()

