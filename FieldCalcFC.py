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
existingFeatureClassField_array = arcpy.GetParameterAsText(2)
existingFeatureClassExp_array = arcpy.GetParameterAsText(3)


#Creates array for Feature Classes
ExistingfeatureClass_array_split = re.sub("[ ;]", " ", existingFeatureClass_array)
arcpy.AddMessage(ExistingfeatureClass_array_split)
ExistingfeatureClass_array_split2 = (ExistingfeatureClass_array_split.split())
arcpy.AddMessage(ExistingfeatureClass_array_split2)

#Creates array for Fields
featureClassField_array_split = re.sub("[ ;.]", " ", existingFeatureClassField_array)
featureClassField_array_split2 = (featureClassField_array_split.split())
arcpy.AddMessage(featureClassField_array_split2)

#Creates array for Expression
featureClassExp_array_split = re.sub("[ ;.]", " ", existingFeatureClassExp_array)
featureClassExp_array_split2 = (featureClassExp_array_split.split())
arcpy.AddMessage(featureClassExp_array_split2)

# Local variables:
db_path = r"C:\Users\dstarr\Documents\ArcGIS\Projects\PortofCleveland"
dataset_path = r"C:\Users\dstarr\Documents\ArcGIS\Projects\PortofCleveland/"+arcpy.env.workspace


# Process: Create Feature Classes
arcpy.AddMessage("Field Calc for Feature Classes")
for existingfcField_array, existingfcExp_array in zip(featureClassField_array_split2, featureClassExp_array_split2):
    expression = '"' + existingfcExp_array+'"'
    arcpy.AddMessage(expression)
    # Process: Calculate Field
    arcpy.CalculateField_management(in_table=existingFeatureClass_array, field=existingfcField_array, expression=expression, expression_type="PYTHON3", code_block="")



