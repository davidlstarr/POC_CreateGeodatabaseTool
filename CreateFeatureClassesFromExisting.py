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
FeatureClassTemplate = arcpy.GetParameterAsText(1)
dataset = arcpy.GetParameterAsText(2)
existingFeatureClass_array = arcpy.GetParameterAsText(3)
featureClass_array = arcpy.GetParameterAsText(4)
geometry_array = arcpy.GetParameterAsText(5)

#Creates array for Feature Classes
ExistingfeatureClass_array_split = re.sub("[ ;]", " ", existingFeatureClass_array)
arcpy.AddMessage(ExistingfeatureClass_array_split)
ExistingfeatureClass_array_split2 = (ExistingfeatureClass_array_split.split())
arcpy.AddMessage(ExistingfeatureClass_array_split2)

#Creates array for Feature Classes
featureClass_array_split = re.sub("[ ;.]", " ", featureClass_array)
featureClass_array_split2 = (featureClass_array_split.split())
arcpy.AddMessage(featureClass_array_split2)

#Creates array for Geometry
geometry_array_split = re.sub("[ ;.]", " ", geometry_array)
geometry_array_split2 = (geometry_array_split.split())
arcpy.AddMessage(geometry_array_split2)

# Local variables:
db_path = r"C:\Users\dstarr\Documents\ArcGIS\Projects\PortofCleveland"
dataset_path = r"C:\Users\dstarr\Documents\ArcGIS\Projects\PortofCleveland/"+arcpy.env.workspace

# Process: Create Feature Classes
arcpy.AddMessage("Create Feature Classes")
for fc_array_layers, geometry_array_list, existingfc_array in zip(featureClass_array_split2, geometry_array_split2, ExistingfeatureClass_array_split2):
    arcpy.Delete_management(fc_array_layers)
    arcpy.CreateFeatureclass_management(out_path=dataset, out_name=fc_array_layers,
                                        geometry_type=geometry_array_list,
                                        template=FeatureClassTemplate,
                                        has_m="DISABLED", has_z="DISABLED",
                                        spatial_reference="PROJCS['NAD_1983_StatePlane_Ohio_North_FIPS_3401_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',1968500.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-82.5],PARAMETER['Standard_Parallel_1',40.43333333333333],PARAMETER['Standard_Parallel_2',41.7],PARAMETER['Latitude_Of_Origin',39.66666666666666],UNIT['Foot_US',0.3048006096012192]];-118963900 -96373800 3048.00609601219;-100000 3048.00609601219;-100000 10000;3.28083333333333E-03;3.28083333333333E-03;0.001;IsHighPrecision",
                                        config_keyword="", spatial_grid_1="0", spatial_grid_2="0", spatial_grid_3="0",
                                        out_alias="")

    fc = arcpy.env.workspace+"/"+fc_array_layers
    #arcpy.AddMessage(fc)

    et_message = "Enable Editor Tracking -- "+fc_array_layers
    arcpy.AddMessage(et_message)
    # Process: Enable Editor Tracking
    arcpy.EnableEditorTracking_management(in_dataset=fc, creator_field="CREATED_BY", creation_date_field="CREATION_DATE", last_editor_field="LAST_EDITED_BY", last_edit_date_field="LAST_EDITED", add_fields="NO_ADD_FIELDS", record_dates_in="DATABASE_TIME")

    at_message = "Add Attribute Rules -- "+fc_array_layers
    arcpy.AddMessage(at_message)

    # Process: Add Attribute Rule
    arcpy.AddAttributeRule_management(in_table=fc, name="UniqueID", type="CALCULATION", script_expression="$feature.DATASET_TYPE + $feature.FEATURE_TYPE + Text(Now(), 'YMDSSS') +Text($feature.OBJECTID, '000');", is_editable="EDITABLE", triggering_events="INSERT;DELETE;UPDATE", error_number="", error_message="", description="", subtype="ALL", field="CCCPA_ID", exclude_from_client_evaluation="INCLUDE", batch="NOT_BATCH", severity="", tags="")

    join_message = "Add Join -- " + fc_array_layers
    arcpy.AddMessage(join_message)
    # Process: Join Field
    arcpy.JoinField_management(in_data=fc, in_field="OBJECTID", join_table=existingfc_array, join_field="OBJECTID", fields="")

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
                    arcpy.AlterField_management(fc, field3.name, str(field3.name).upper() + "_2",
                                                str(field3.aliasName).upper())
                    arcpy.AlterField_management(fc, field3.name + "_2", str(field3.name).upper(),
                                                str(field3.aliasName).upper())
                    arcpy.AlterField_management(fc, field3.name, str(field3.name).upper(),
                                                str(field3.aliasName).upper())
                    arcpy.AddMessage("\tUpdated {0}".format(field3.name))
            except:
                arcpy.AddMessage("\tUnable to update {0}".format(field3.name))
                pass








