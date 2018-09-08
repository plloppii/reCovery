from tkinter import filedialog
from tkinter import *
import os.path

root = Tk()

root.fileName = filedialog.askopenfilename(filetypes = (("Gcode files","*.gcode"),("all files","*.*")))

print(root.fileName)

recovery = open(root.fileName,"r")
for line in recovery:
	print(line)