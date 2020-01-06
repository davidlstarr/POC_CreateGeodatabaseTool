# -*- coding: utf-8 -*-
"""
Create Feature Classes from existing Feature Classes
"""

import arcpy
import re

# To allow overwriting the outputs change the overwrite option to true.
arcpy.env.overwriteOutput = False

# Script parameters
arcpy.env.workspace = arcpy.GetParameterAsText(0)
existingFeatureClass_array = arcpy.GetParameterAsText(1)


#Creates array for Feature Classes
ExistingfeatureClass_array_split = re.sub("[ ;]", " ", existingFeatureClass_array)
arcpy.AddMessage(ExistingfeatureClass_array_split)
ExistingfeatureClass_array_split2 = (ExistingfeatureClass_array_split.split())
arcpy.AddMessage(ExistingfeatureClass_array_split2)

# Local variables:
db_path = r"C:\Users\dstarr\Documents\ArcGIS\Projects\PortofCleveland"
dataset_path = r"C:\Users\dstarr\Documents\ArcGIS\Projects\PortofCleveland/"+arcpy.env.workspace

# Process: Create Feature Classes
arcpy.AddMessage("Create Feature Classes")
for fc_array_layers in ExistingfeatureClass_array_split2:

    fc = fc_array_layers
    #arcpy.AddMessage(fc)

    #Remove Duplicate Fields after join
    removeMessage = "Removing duplicate fields"
    arcpy.AddMessage(removeMessage)

    #variables
    fieldObjList = arcpy.ListFields(fc)
    fieldNameList = []
    fieldRemoveList = []

    for field in fieldObjList:
        if not field.required:
            fieldNameList.append(field.name)

    for field2 in fieldNameList:
        if '_1' in field2:
            fieldRemoveList.append(field2)

    if len(fieldRemoveList) != 0:
        arcpy.AddMessage(fieldRemoveList)
        arcpy.DeleteField_management(in_table=fc, drop_field=fieldRemoveList)
    else:
        message = fc_array_layers + " -- does not contain duplicate fields."
        arcpy.AddMessage(message)

    #Uppercase all aliases and remove duplicate DATASOURCE field
    arcpy.AddMessage("Text to uppercase all aliases in feature class and remove duplicate DATASOURCE field.")
    for field3 in fieldObjList:
        if not field3.required:
            try:
                if field3.name == "DATASOURCE":
                    # Remove duplicate DATASOURCE field
                    arcpy.AddMessage("Remove duplicate DATASOURCE field")
                    arcpy.DeleteField_management(in_table=fc, drop_field="DATASOURCE")
                if field3.name != "" or field3.aliasName != "":
                    arcpy.AddMessage(str(field3.name).upper())
                    arcpy.AlterField_management(fc, field3.name, str(field3.name).upper()+"_2", str(field3.aliasName).upper())
                    arcpy.AlterField_management(fc, field3.name+"_2", str(field3.name).upper(), str(field3.aliasName).upper())
                    arcpy.AlterField_management(fc, field3.name, str(field3.name).upper(), str(field3.aliasName).upper())
                    arcpy.AddMessage("\tUpdated {0}".format(field3.name))

            except:
                arcpy.AddMessage("\tUnable to update {0}".format(field3.name))
                pass








