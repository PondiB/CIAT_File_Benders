# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# RasCal.py
# Created on: 2014-09-09 15:00:31.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import os
import arcpy
from arcpy import env


class ModisMeanCalc(object):
    """Search for MODIS .tif file and calculate mean raster using ArcGIS Cell Statistics"""

    def get_file_paths(self):
        """Returns MODIS file paths"""
        tiff_dirs = []
        counter = 0
        for root_path, dir_names, files in os.walk("D:\\Data\\Modis"):
            for dir_name in dir_names:
                for dir_Output in dir_name.split("_"):
                    if dir_Output == "TIFF":
                        dir_join = os.path.join(root_path, dir_name).replace("\\","/")
                        tiff_dirs.append(dir_join)
        return tiff_dirs

    def get_files(self):
        """Get files and calculate mean using cell statistics gp"""
        for source_path in self.get_file_paths():
            ras_input = []
            for file in os.listdir(source_path):
                if file.startswith('MOD_') & file.endswith('.tif'):
                    file_path = os.path.join(source_path, file).replace("\\","/")
                    ras_input.append(file_path)
            out_ras = source_path + "/MEAN_MOD_" + source_path[-4:] + ".tif"
            print("CALCULATING MEAN FOR ......... " + source_path[-4:])
            arcpy.gp.CellStatistics_sa(ras_input, out_ras, "MEAN", "DATA")
        print("PROCESSING COMPLETED SUCCESSFULLY!!!")

def main():
    """Main program"""
    # Check out any necessary licenses
    env.overwriteOutput = True
    arcpy.CheckOutExtension("spatial")
    f_tif = ModisMeanCalc()
    f_tif.get_files()

if __name__ == "__main__":
    main()
    




