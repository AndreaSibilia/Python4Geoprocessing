#### RIVER 3D PROFILES TOOL ####
## Build through PyCharm v2017.3.3 ##

# Import the ArcPy site package
import arcpy

# Check availability of the 3D extension (try/except comes from ESRI Help)
# Source: "http://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-functions/checkextension.htm"
class LicenseError(Exception):
    pass

try:
    ''' If the 3D extension is available the tool performs its tasks
    otherwise it raises the custom error LicenseError'''

    if arcpy.CheckExtension("3D") == "Available":
        arcpy.CheckOutExtension("3D")
    else:
        raise LicenseError


    '''Process starts'''

    # Ask the user if he prefers to set up a common workspace to avoid to insert the whole path for each file.
    while True:

        '''Handling value errors: the user must insert y/Y if he wants to
        set the workspace or n/N if he doesn't want to set it. Other values
        are not allowed.'''

        pathQuestion = raw_input("Would you like to specify a defined workspace (insert y/n or Y/N )?: ")
        if pathQuestion in ("y","Y","n","N"):
            break
        else:
            print("\nYou must insert y/Y if yes or n/N if no. Numerical values are not allowed.\n")

    '''Check the user's answer: if yes he has to insert the path of the workspace'''

    if pathQuestion == "y" or pathQuestion == "Y":
        '''If the user answers yes (y/Y), then the tool asks for the path;
        otherwise it just goes on and asks for the parameters.'''

        ws = raw_input("Please insert the path of your workspace: ")
        arcpy.env.workspace = r"%s" %ws
        print("\nWARNING: You will need to specify just the name of your input file. \n"
              "WARNING: You can define a different folder for your output; in this case, the full path must be entered.\n")

    elif pathQuestion == "n" or pathQuestion == "N":
        print("\nWARNING: You must insert the full path for both the input and the output files.\n")

    # The tool overwrites the outputs
    arcpy.env.overwriteOutput = True

    # Set up all the input file required for the analysis
    lineFeature = raw_input("Please, insert the line feature: ")
    negOff = raw_input("Please, insert the list of negative offsets: ")
    posOff = raw_input("Please, insert the list of positive offsets: ")
    offsetsList = [negOff, posOff]
    output1 = raw_input("Insert (the path and) the name of the output Route Layer: ")
    output2 = raw_input("Insert (the path and) the name of the output Points Layer: ")
    output3 = raw_input("Insert (the path and) the name of the output Points to Line Layer: ")
    dtm = raw_input("Insert (the path and) the name of the input surface:" )
    output4 = raw_input("Insert (the path and) the name of the Final Output: ")

    # Create a route tool from the lineFeature
    arcpy.CreateRoutes_lr(lineFeature, "Route", output1)

    # Make a route event layer for each bank
    outList = []
    for i in offsetsList:
        arcpy.MakeRouteEventLayer_lr(output1, "Route", i, "route POINT LOCATION", i+"route", "OFFSET", "", "", "",
                                 "", "", "POINT")
        outList.append(i+"route")
        '''Merge the results to create a feature class containing all the points
        that will be used to create the transversal profiles'''
        arcpy.Merge_management(outList, output2)

    # Create the 3D transversal profiles
    '''1 - Convert the points to line. The lines are created by using the field "LOCATION" derived from the input table;
    2 - The lines are interpolated with the DTM, thus a new 3D feature class is created'''
    arcpy.PointsToLine_management(output2, output3, "LOCATION")
    arcpy.InterpolateShape_3d(dtm, output3, output4)

    '''Process finishes'''

except LicenseError:
    print("3D Analyst license is unavailable")
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
