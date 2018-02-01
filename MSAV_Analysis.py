#### MULTIPLE SURFACES AREA&VOLUME ANALYSIS TOOL ####
## Build with PyCharm v2017.3.3 ##

# Import ArcPy site package
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
        otherwise it just goes on and asks for the parameters.'''

        ws = raw_input("Please insert the path of your workspace: ")
        arcpy.env.workspace = r"%s" %ws
        print("WARNING: You will need to specify just the name of your input file. \n"
              "WARNING: You can define a different folder for your output; in this case, the full path must be entered.\n"
              "WARNING: Remember to set the output with .txt extension.\n")

    elif pathQuestion=="n" or pathQuestion=="N":
        print("WARNING: You must insert the full path for both the input and the output files.\n"
              "WARNING: Remember to set the output with .txt extension.\n")

    # Allow the tool to overwrite the output; this is necessary to write a txt file with multiple lines
    arcpy.env.overwriteOutput = True

    # Set up a list which contains all the values whereby the user wants to perform the Area&Volume calculation
    while True:
        '''The user can directly run the tool to get the results.
        The tool asks for the input parameters and the output and then it performs the analysis'''
        try:
            basePlane = int(raw_input("Enter the value of the base plane (value must be in cm): ")) # The value MUST be in cm
            topPlane = int(raw_input("Enter the value of the last plane (value must be in cm): ")) # The value MUST be in cm
            step = int(raw_input("Enter the value to determine the step (value must be in cm): ")) # The value MUST be in cm
        except ValueError:
            print("The value must be an integer")
            continue
        else:
            break

    # Create the list of values required to perform the Area&Volume analysis
    values= range(basePlane, topPlane, step)

    # Convert the values of the list from integers to floats and store them in
    # an another list that will be used by the Surface Volume tool
    valDef = []
    for v in values:
        v=float(v)
        valDef.append(v/100)

    # Perform the Area&Volume analysis; the Python tool asks the user for the input and output file
    input = raw_input("Please, insert the input surface: ")
    output = raw_input("Please, insert the output text (.txt) file: ")
    for i in valDef:
        arcpy.SurfaceVolume_3d(in_surface=input, out_text_file=output, reference_plane="BELOW", base_z=i,
                               z_factor="1", pyramid_level_resolution="0")

    '''Process finishes'''

except LicenseError:
    print("3D Analyst license is unavailable")
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
