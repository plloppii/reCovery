from cx_Freeze import setup, Executable

import sys
import os

os.environ['TCL_LIBRARY'] = "C:\\Users\\Noah\\Miniconda3\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\Noah\\Miniconda3\\tcl\\tk8.6"

if sys.platform=='win32':
    base = "Win32GUI"

target = Executable(
    script="Controller.py",
    base= base,
    icon="re3d.ico"
    )

build_exe_options = {"includes": ["tkinter"],"include_files": ["tcl86t.dll", "tk86t.dll","re3D.png"]}
setup(
	name = "re:3D_reCovery",
	version = "1.0",
	description = "A gcode recovery application used to recover failed 3D prints",
	options = {"build_exe": build_exe_options},
	executables = [target] )
