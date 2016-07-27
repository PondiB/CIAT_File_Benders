__author__ = "Koech Nicholas"
__copyright__ = "Copyright 2016"
__email__ = "koechnicholas@gmail.com"
__status__ = "draft"


import arcpy
from arcpy import env
from arcpy.sa import *
from filelocation import get_file_location
import ntpath
import os
from readjson import get_json_data
from sourcedirectory import get_directory
import traceback
import sys


class TrendCorrelation:
    def __init__(self):
        self.tool_settings = self._get_user_parameters()
        self.data_var = ['var_1', 'var_2']
        self.src_var_1 = self.tool_settings['src_dir_1']
        self.dir_startswith_var_1 = self.tool_settings['dir_startswith_1']
        self.file_startswith_var_1 = self.tool_settings['file_startswith_1']
        self.file_endswith_var_1 = self.tool_settings['file_endswith_1']
        self.src_var_2 = self.tool_settings['src_dir_2']
        self.dir_startswith_var_2 = self.tool_settings['dir_startswith_2']
        self.file_startswith_var_2 = self.tool_settings['file_startswith_2']
        self.file_endswith_var_2 = self.tool_settings['file_endswith_2']
        self.dest_dir = self.tool_settings['dest_dir']
        self.place_name = self.tool_settings['aoi_place_name']

    def _get_user_parameters(self):
        """Get contents from a Json file"""
        tool_settings = {}
        data = get_json_data('dir_meta', '.json')
        for i in data:
            for j in data[i]:
                if isinstance(j, dict):
                    tool_settings.update(j)
        return tool_settings

    def init_geoprocess_raster(self):
        """ Initialize raster geoprocessing """
        cell_size = self.validate_data()  # Validated raster

        # if not os.path.exists(self.dest_dir):
        #     os.makedirs(self.dest_dir)  # Create destination folder
        print('RASTER PROCESSING COMPLETED SUCCESSFULLY!!!')

    def validate_data(self):
        """ Check for  invalid/corrupted data """
        prev_file_path = ''
        ras_resolution = []
        for root_dir, file_startswith, file_endswith in self._get_source_parameters(self.data_var):
            for source_dir, file_path, file_name in get_file_location(root_dir, file_startswith, file_endswith):
                self._validate_spatial_ref(file_path, prev_file_path)
                print('Validated..... {0}'.format(file_name))
                cell_size = self._get_raster_resolution(file_path, ras_resolution)  # Get raster resolution
                if cell_size:
                    ras_resolution.append(cell_size)
                prev_file_path = file_path
        self._validated_place_name()  # validated area of interest name as three letter acronym
        return ras_resolution

    def _get_source_parameters(self, data_var):
        """ Get files root directory """
        for i in data_var:
            if i == 'var_1':
                root_dir = get_directory(self.src_var_1, self.dir_startswith_var_1)
                file_startswith = self.file_startswith_var_1
                file_endswith = self.file_endswith_var_1
                yield root_dir, file_startswith, file_endswith
            else:
                root_dir = get_directory(self.src_var_2, self.dir_startswith_var_2)
                file_startswith = self.file_startswith_var_2
                file_endswith = self.file_endswith_var_2
                yield root_dir, file_startswith, file_endswith

    def _validate_spatial_ref(self, file_path, prev_file_path):
        """ Get raster spatial reference """
        try:
            current_spatial_ref = self._get_spatial_ref(file_path)
            if prev_file_path:
                prev_spatial_ref = self._get_spatial_ref(prev_file_path)
                try:
                    if current_spatial_ref.factoryCode == prev_spatial_ref.factoryCode:
                        return current_spatial_ref
                    else:
                        raise ValueError("{} has a different spatial reference. Please correct it and run the process again".format(file_path))
                except ValueError, e:
                    sys.exit(e)
            else:
                return current_spatial_ref
        except IOError as (e):
            print(str(e) + ' or is invalid/corrupted. Remove the bad file and run the process again')

    def _get_spatial_ref(self, file_path):
        """ Describe raster spatial reference """
        return arcpy.Describe(file_path).spatialReference

    def _get_raster_resolution(self, file_path, ras_resolution):
        """ Get all raster files resolution """
        cell_width = self._get_cell_width(file_path)
        if ras_resolution:
            if cell_width not in set(ras_resolution):
                return cell_width
        else:
            return cell_width

    def _validated_place_name(self):
        """ Check place name acronym """
        try:
            if len(self.place_name) != 3:
                raise ValueError('Input value "{0}" should be made of three characters'.format(self.place_name))
        except ValueError as e:
            print(e)

    def _get_cell_width(self, file_path):
        """ Get raster cell size """
        return arcpy.Describe(file_path).meanCellWidth

    def _delete_raster_file(self, in_file):
        """ Delete extracted file """
        for extracted_file in in_file:
            arcpy.Delete_management(extracted_file)


def main():
    """Main program"""
    env.overwriteOutput = True
    arcpy.CheckOutExtension("spatial")
    read_file = TrendCorrelation()
    read_file.init_geoprocess_raster()

if __name__ == '__main__':
    main()