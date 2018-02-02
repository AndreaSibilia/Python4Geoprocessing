#### POLYGONS EXTRACTION FROM A RASTER ####
## Build with PyCharm v2017.3.3 ##

# Import the libraries required for the analysis
import arcpy
from arcpy import env
from arcpy.sa import *

# Retrieve the spatial analyst extension
arcpy.CheckOutExtension("Spatial")

# The tools ask to the user if he wants to set the workspace before to perform the analysis
while True:

    '''Handling value errors: the user must insert y/Y if he wants to
    set the workspace or n/N if he doesn't want to set it. Other values
    are not allowed.'''

    pathQuestion = raw_input("Would you like to specify a defined workspace (insert y/n or Y/N )?: ")
    if pathQuestion in ("y","Y","n","N"):
        break
    else:
        print("\nYou must insert y/Y if yes or n/N if no. Numerical values are not allowed.\n")

if pathQuestion=="y" or pathQuestion=="Y":

    '''If the user answers yes (y/Y), then the tool asks for the path;
    otherwise it just goes on and asks for other parameters.'''

    ws = raw_input("Please insert the path of your workspace: ")
    env.workspace = r"%s" %ws
    print("WARNING: You will need to specify just the name of your input file. \n"
          "WARNING: You can define a different folder for your in/output, anyway; in this case, the full path must be entered.\n")

elif pathQuestion=="n" or pathQuestion=="N":
    print("WARNING: You must insert the full path for your in/output files.\n")

# Allow the tool to overwrite the output; this is necessary to write a txt file with multiple lines
env.overwriteOutput = True

# Set up the variables required to perform all the tasks

while True:

    '''The tool asks for a "closing section": ths parameter is compulsory only if the contour lines
    do not describe a closed path. In this case the polygon cannot be generated; the closing
    section allows to intersect the contour lines in order to define a closed path'''

    closingSection = raw_input("A closing section is required to draw the polygons (True or False): ")
    if closingSection == "True" or closingSection == "T" or closingSection == "true" or closingSection == "t":
        closingSectionFeature = raw_input("Enter the closing section feature (polygon or polyline): ")
        break
    elif closingSection == "False" or closingSection == "F" or closingSection == "false" or closingSection == "f":
        break
    else:
        print("\nError: incorrect value entered\n"
              "Only True or False are allowed.\n")

# Set up the list of values which represent the altitude of the contour lines
while True:
    '''The tool starts to define the contour from the base plane and draws a contour
    for each interval defined by the step. The tool stops to run when it reaches the
    top plane --> The top plane IS NOT INCLUDED!'''
    try:
        basePlane = int(raw_input("Enter the value of the base plane (value must be in cm): "))
        topPlane = int(raw_input("Enter the value of the last plane (value must be in cm): "))
        step = int(raw_input("Enter the value to determine the step (value must be in cm): "))
    except ValueError:
        print("\nError: the value must be an integer\n")
        continue
    else:
        break

valuesCm = range(basePlane, topPlane, step)

# Set the parameters required to perform both the Contour list and the Feature to polygon tools
inputSurface = raw_input("Enter the input surface raster: ")
outputContourLine = raw_input("Enter the output contour polyline: ")
outputPolygon = raw_input("Enter the output polygon feature class: ")


# Define a function to convert the contour values from centimeters to metes
def convertValuesMeter(list):
    valuesM = []
    for val in list:
        val = float(val)
        valuesM.append(val/100)
    return valuesM

# Define a function that performs both the Contour list an the Feature to polygon tools
def polygonExtraction(list, closure):
    outputContourList = []
    outputPolygonList = []
    for number in list:
        '''For each altitude value stored within the valuesCm list, the loop
        create a contour line'''
        ContourList(inputSurface, outputContourLine + "_" + str(int(number * 100)), number)
        outputContourList.append(outputContourLine + "_" + str(int(number * 100)))

        for var in outputContourList:
            '''The for loop prints what it is processing'''
            outputPolygonList.append(var[-3:])
        print "Processing value (contour) " + outputPolygonList[-1]

    for i in outputContourList:
        '''A polygon is generated for each contour line previously created.
        The if statement verifies if the closing section features is required or not'''
        if closure == "True" or closure == "T" or closure == "true" or closure == "t":
            arcpy.FeatureToPolygon_management([i, closingSectionFeature], outputPolygon+i[-4:])
            print "Processing value (polygon) " + i[-3:]
        else:
            arcpy.FeatureToPolygon_management(i, outputPolygon + i[-4:])
            print "Processing value (polygon) " + i[-3:]

# Run the function to get the results
polygonExtraction(convertValuesMeter(valuesCm), closingSection)

# Return the license to the License Manager to make it available for other applications
arcpy.CheckInExtension("spatial")