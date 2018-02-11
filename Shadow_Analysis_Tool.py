#### SHADOW ANALYSIS TOOL ####
## Build through PyCharm v2017.3.3 ##


#### Import the required libraries ####
import os
import csv
import arcpy


#### Set up the workspace ####
# Check if the 3D extension is licensed
arcpy.CheckOutExtension("3D")
# Allow the tool to overwrite the output
arcpy.env.overwriteOutput = True


#### Import the csv with the Sun path parameters (time, elevation, azimuth) ####
# Ask for the csv Path and Name; they must be string
while True:
    try:
        csv_path = raw_input("Path to the \".csv\" file: ")
        csv_name = raw_input("Name of the \".csv\" file: ")
    except ValueError:
        print("\nPath and name must be a string value")
    else:
        break
# Open the CSV file. Each row is store as a list within a list that contains all the rows
os.chdir(r"%s" %csv_path)
with open(csv_name) as csvfile:
    reader = csv.reader(csvfile)
    parameters = [[str(row[0]), float(row[1]), float(row[2])] for row in reader]
print "\nHere is the imported CSV:"
print str(parameters) + "\n"


#### Define the parameters to perform the Hillshade analysis ####
# Set up the Hillshade workspace environment
while True:
    try:
        ws = raw_input("Path to the workspace environment: ")
        arcpy.env.workspace = r"%s" %ws
        print("WARNING: You can define a different folder for your in/output, anyway; in this case, the full path must be entered.\n")
    except ValueError:
        print("\nPath must be a string value")
    else:
        break
# Input surface (i.e. DTM, DSM)
input =  raw_input("Input surface: ")
# Output file name; this must be a string value, otherwise the Hillshade does not work
while True:
    try:
        output_name = str(raw_input("Output file name: "))
    except ValueError:
        print("\nOutput fle name must be a string value")
    else:
        break


#### Hillshade analysis for the shadows ####
for i in parameters:
    arcpy.HillShade_3d(input,
                       output_name+i[0][:2]+"-"+i[0][3:5], i[2], i[1], "SHADOWS", 1)