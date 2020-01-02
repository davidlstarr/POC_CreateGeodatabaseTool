# -*- coding: utf-8 -*-
"""
Generate attribute rules for every feature class in the geodatabase
"""

import arcpy
import os

# To allow overwriting the outputs change the overwrite option to true.
arcpy.env.overwriteOutput = False

# Script parameters
arcpy.env.workspace = arcpy.GetParameterAsText(0)

# Local variables:
datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []
arcpy.AddMessage("Create Attribute Rules for All Feature Classes")

#Generate attribute rules
for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        arcpy.AddMessage(path)
        at_message = "Add Attribute Rules -- " + path
        arcpy.AddMessage(at_message)

        # Process: Add Attribute Rule
        arcpy.AlterAttributeRule_management(in_table=path, name="UniqueID", description="", error_number="", error_message="", tags="", triggering_events="INSERT;UPDATE;DELETE", script_expression="$feature.DATASET_TYPE + $feature.FEATURE_TYPE + Text(Now(), 'YMDSSS') +Text($feature.OBJECTID, '000');")






