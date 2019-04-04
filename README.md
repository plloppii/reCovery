# Gcode reCovery Application
<img src=img/Interface.JPG alt= "AppScreenshot" width = "500" >

A gcode recovery application that helps users recover failed printers by reformatting their gcode file. 
Whether your machine stopped printing because the power went out or the machine had a filament jam, the reCovery application can recover the print. By measuring the height of the model and inputting this measurement into the application along with the original gcode file, the application will generate a new recovery file that will recover the failed 3D print. 

Requirements: Windows 7+, SD card driven 3D printer, Approximate height of failed 3D print through measurement

Instructions for use:

1) Download application through release/gcode_reCovery.exe
2) Run as administrator
3) Input Gcode file of failed 3D print
4) Input approximate height of failed 3D print
5) Input if the print reset due to Power Outtage or not
6) Click Process Gcode
7) Select the desired layer height to resume on
8) Click Generate reCovery File for the file to be placed within the location of the original file
9) Run the recovery file in your 3D printer to recover the failed 3D print

