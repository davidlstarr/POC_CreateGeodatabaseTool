# -*- coding: utf-8 -*-
"""
Create a master geodatabase and corresponding datasets
"""

import arcpy
import re

# To allow overwriting the outputs change the overwrite option to true.
arcpy.env.overwriteOutput = False

# Script parameters
arcpy.env.workspace = arcpy.GetParameterAsText(0)
FeatureClassTemplate = arcpy.GetParameterAsText(1)
dataset_array = arcpy.GetParameterAsText(2)
# featureClass_array = arcpy.GetParameterAsText(3)
# geometry_array = arcpy.GetParameterAsText(4)

#Creates array for Datasets
dataset_array_split = re.sub("[ ;.]", " ", dataset_array)
dataset_array_split2 = (dataset_array_split.split())
arcpy.AddMessage(dataset_array_split2)


# #Creates array for Feature Classes
# featureClass_array_split = re.sub("[ ;.]", " ", featureClass_array)
# featureClass_array_split2 = (featureClass_array_split.split())
# arcpy.AddMessage(featureClass_array_split2)
#
# #Creates array for Geometry
# geometry_array_split = re.sub("[ ;.]", " ", geometry_array)
# geometry_array_split2 = (geometry_array_split.split())
# arcpy.AddMessage(geometry_array_split2)



# Local variables:
db_path = r"C:\Users\dstarr\Documents\ArcGIS\Projects\PortofCleveland"
dataset_path = r"C:\Users\dstarr\Documents\ArcGIS\Projects\PortofCleveland/"+arcpy.env.workspace

# Process: Create File Geodatabase
arcpy.AddMessage("Create File Geodatabase")
arcpy.Delete_management(dataset_path)
arcpy.CreateFileGDB_management(out_folder_path=db_path, out_name=arcpy.env.workspace, out_version="CURRENT")

# Process: Create Feature Datasets
arcpy.AddMessage("Create Feature Datasets")
for dataset_array_layers in dataset_array_split2:
    arcpy.CreateFeatureDataset_management(out_dataset_path=dataset_path, out_name=dataset_array_layers,
                                          spatial_reference="PROJCS['NAD_1983_StatePlane_Ohio_North_FIPS_3401_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',1968500.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-82.5],PARAMETER['Standard_Parallel_1',40.43333333333333],PARAMETER['Standard_Parallel_2',41.7],PARAMETER['Latitude_Of_Origin',39.66666666666666],UNIT['Foot_US',0.3048006096012192]];-118963900 -96373800 3048.00609601219;-100000 3048.00609601219;-100000 10000;3.28083333333333E-03;3.28083333333333E-03;0.001;IsHighPrecision")

# Process: Create Feature Classes
arcpy.AddMessage("Create Feature Classes")
# for dataset_array_layers, fc_array_layers, geometry_array_list in zip(dataset_array_split2, featureClass_array_split2, geometry_array_split2):
#     arcpy.CreateFeatureclass_management(out_path=dataset_array_layers, out_name=fc_array_layers,
#                                         geometry_type=geometry_array_list,
#                                         template=FeatureClassTemplate,
#                                         has_m="DISABLED", has_z="DISABLED",
#                                         spatial_reference="PROJCS['NAD_1983_StatePlane_Ohio_North_FIPS_3401_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',1968500.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-82.5],PARAMETER['Standard_Parallel_1',40.43333333333333],PARAMETER['Standard_Parallel_2',41.7],PARAMETER['Latitude_Of_Origin',39.66666666666666],UNIT['Foot_US',0.3048006096012192]];-118963900 -96373800 3048.00609601219;-100000 3048.00609601219;-100000 10000;3.28083333333333E-03;3.28083333333333E-03;0.001;IsHighPrecision",
#                                         config_keyword="", spatial_grid_1="0", spatial_grid_2="0", spatial_grid_3="0",
#                                         out_alias="")

arcpy.AddWarning("Move Feature Class Template into Created gdb")