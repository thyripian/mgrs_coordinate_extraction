# Python Core - Backend Package

import os, sys
import re
import pandas as pd
import numpy as np
import simplekml
import zipfile
import zlib
import mgrs
from datetime import datetime
import openpyxl

'''
EXTRACTION creates mgrs_dict, mgrs_df
'''

class EXTRACTION:
    def __init__(self,fpaths,fextensions):
        mgrs_dict, _mgrs = {}, []
        
        for key, value in fpaths.items():
        input_file = value
        extension = fextensions[key]
        name = fpaths[key]
        self.input_file = input_file
        self.name = name
        
        mgrs_to_dict(self,input_file,extension,name,mgrs_dict)
        for item in self.mgrs_temp:
            _mgrs.append(item)
         
        self._mgrs = _mgrs
    mgrs_dict['extracted_coordinates'] = self._mgrs
    self.mgrs_dict = mgrs_dict
    self.mgrs_df = mgrs_df
    
def mgrs_to_dict(self,input_file,extension,name,mgrs_dict):
    
    mgrs_temp = []
    
    space_pattern = (r'(([0-9]{2})([A-Z]{2})\s([0-9]*)\s([0-9]*))')
    no_space_pattern = (r'(([0-9]{2})([A_Z]{3})([0-9]{1}[0-9]*))')
    
    def csv_or_xlsx(self,input_file,extension):
        
        # NOTE: if your input file does not have a title row, set header to zero (0)
        
        if extension == '.csv':
            df = pd.read_csv(input_file,header=1,encoding='latin') 
        
        elif extension == '.xlsx':
            df = pd.read_excel(input_file,header=1,engine='openpyxl')
            
        i=0
        
        while i in range(len(df.columns)):
            col = df.columns[i]
            
            for row in df[f'{col}']:
                if type(row) == str:
                    space_match = re.search(space_pattern,row)
                    no_space_math = re.search(no_space_pattern,row)
                    
                    if space_match:
                        if str(space_match.group()).replace(' ','') not in mgrs_temp:
                            grid = str(space_match.group()).replace(' ','')
                            mgrs_temp.append(grid)
                        else:
                            pass
                            
                    elif no_space_match:
                        if no_space_match.group() not in mgrs_temp:
                            mgrs_temp.append(no_space_match.group())
                        else:
                            pass
                           
                    else:
                        pass
                        
            i += 1
            self.mgrs_temp = mgrs_temp
            
    def text(self,input_file,extension):
        
        with open(input_file,'r') as file:
            
            for line in file.readlines():
                space_match = re.search(space_pattern,line)
                no_space_match = re.search(no_space_pattern,line)
                
                if space_match:
                    if str(space_match.group()).replace(' ','') not in mgrs_temp:
                        grid = str(space_match.group()).replace(' ','')
                        mgrs_temp.append(grid)
                    else:
                        pass
                        
                elif no_space_match:
                    if no_space_match.group() not in mgrs_temp:
                        mgrs_temp.append(no_space_match.group())
                    else:
                        pass
                        
                else:
                    pass
            self.mgrs_temp = mgrs_temp
            
    if extension == '.xlsx' or extension == '.csv':
        csv_or_xlsx(self,input_file,extension)
    elif extension == '.txt':
        text(self,input_file,extension)
        
    mgrs_dict['extracted_coordinates'] = mgrs_temp
    
    self.mgrs_dict = mgrs_dict
    
    return self.mgrs_dict
    
    
###############
'''
CONVERSION creates latlon_dict, latlon_disp_dict, latlon_df
'''

class CONVERSION:
    def __init__(self,mgrs_dict):
        latlon_list, latlon_dict, latlon_disp_list, latlon_disp_dict = [], {}, [], {}
        
        self.latlon_dict = mgrs_to_latlon_dict(self,mgrs_dict,latlon_dict,latlon_list)
        self.latlon_disp_dict = mgrs_to_latlon_disp_dict(self,mgrs_dict,latlon_disp_dict,latlon_disp_list)
        self.latlon_disp_df = mgrs_to_latlon_disp_df(self,self.latlon_disp_dict)
        self.latlon_df = mgrs_to_latlon_df(self,self.latlon_dict)
        
def mgrs_to_latlon_dict(self,mgrs_dict,latlon_dict,latlon_list):
    self.mgrs_dict = mgrs_dict
    
    for key, value in self.mgrs_dict.items():
        
        try:
            mgrs_object = mgrs.MGRS()
            
            for item in value:
                coord = mgrs_object.toLatLon(item)
                latlon_list.append([item,coord])
        except BaseException:
            pass
                
        latlon_dict[key] = latlon_list
    
    self.latlon_dict = latlon_dict
    
    return self.latlon_dict
        
def mgrs_to_latlon_disp_dict(self,mgrs_dict,latlon_disp_dict,latlon_disp_list):
    self.mgrs_dict = mgrs_dict
    
    for key, value in self.mgrs_dict.items():
    
        try:
            mgrs_object = mgrs.MGRS()
            
            for item in value:
                coord = mgrs_object.toLatLon(item)
                latlon_disp_list.append(str(coord))
        except BaseException:
            pass
    
    self.latlon_disp_dict = latlon_disp_dict
    
    return self.latlon_disp_dict

def mgrs_to_latlon_disp_df(self,latlon_disp_dict):
    latlon_disp_df = pd.DataFrame.from_dict(latlon_disp_dict)
    latlon_disp_df.columns = ['extracted_coordinates']
    self.latlon_disp_df = latlon_disp_df
    return self.latlon_disp_df

def mgrs_to_latlon_df(self,latlon_dict):
    latlon_df = pd.DataFrame.from_dict(latlon_dict)
    self.latlon_df = latlon_df
    return self.latlon_df
    
    
###############
'''
SHAPEFILES creates kmz
'''

class SHAPEFILES:
    def __init__(self,latlon_dict,latlon_df):
        self.kmz = generate_kmz(self,latlon_dict,latlon_df).kmz

def generate_kmz(self,latlon_dict,latlon_df):

    def format_points(self,pnt):
        pnt.style.labelstyle.scale = 0.75
        pnt.style.iconstyle.scale = 0.75
        pnt.style.iconstyle.color = 'ffffff00'
        pnt.style.iconstyle.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
        
    if isinstance(latlon_dict,dict):
        
        data = latlon_df
        kmz = simplekml.Kml()
        
        for item in data.items():
            
            for row in item:
                
                if 'coordinates' in row:
                    pass
                
                else:
                    for pair in row:
                        
                        coord = []
                        coord.append([pair[1][1], pair[1][0]])
                        pnt_name = pair[0]
                        pnt = kmz.newpoint(name=pnt_name,description=pnt_name,coords=coord)
                        format_points(self,pnt)
        
        self.kmz = kmz
        
        return self.kmz
        
###############
'''
TOOLKIT is the parent class of the program. Calls all child classes and performs pre-processing tests.
Also creates dictionaries of file-specific variables based on uploaded data.
'''        

class TOOLKIT:
    def __init__(self,input_file,name)::
        
        fpaths, fextensions = {}, {}
        
        try: 
            if len(input_file) > 1:
                
                for i in range(len(name)):
                    
                    fpaths[name[i]] = str(input_file[i])
                    
                    if name[i].endswith('.xlsx'):
                        fextensions[name[i]] = '.xlsx'
                    elif name[i].endswith('.csv'):
                        fextensions[name[i]] = '.csv'
                    elif name[i].endswith('.txt'):
                        fextensions[name[i]] = '.txt'
                        
                self.fpaths = fpaths
                self.fextensions = fextensions
            else: 
                i = 0
                fpaths[name[i]] = str(input_file[i])
                
                if name[i].endswith('.xlsx'):
                    fextensions[name[i]] = '.xlsx'
                elif name[i].endswith('.csv'):
                    fextensions[name[i]] = '.csv'
                elif name[i].endswith('.txt'):
                    fextensions[name[i]] = '.txt'
                
                self.fpaths = fpaths
                self.fextensions = fextensions
                
            pre_run_test(self,fpaths,fextensions)
            
            if pre_run_test:
                local_extract = EXTRACTION(fpaths,fextensions)
                self.mgrs_dict = local_extract.mgrs_dict
                self.mgrs_df = local_extract.mgrs_df
                self.mgrs_temp = local_extract.mgrs_temp
                self._mgrs = local_extract._mgrs
                
                local_convert = CONVERSION(self.mgrs_dict)
                self.latlon_dict = local_convert.latlon_dict
                self.latlon_disp_dict = local_convert.latlon_disp_dict
                self.latlon_disp_df = local_convert.latlon_disp_df
                self.latlon_dict = local_convert.latlon_dict
                
                local_shape = SHAPEFILES(self.latlon_dict,self.latlon_df)
                self.kmz = local_shape.kmz
                
                self.status = 'Successfully processed all files uploaded.'
            else:
                self.flag
                
        except ValueError as e:
            self.status = 'Failed to process all files. Please try again or remove some of the files.'
            
def pre_run_test(self,fpaths,fextensions):
    
    def ec_test(self,fpaths,fextensions):
        
        try:
            test_extract = EXTRACTION(fpaths,fextensions)
            self.mgrs_dict = test_extract.mgrs_dict
        except BaseException as er1:
            return False
            
        try:
            self.latlon_dict = CONVERSION(self.mgrs_dict).latlon_dict
        except BaseException as er2:
            return False
            
    def kmz_test(self,latlon_dict,latlon_df):
        
        try:
            SHAPEFILES(latlon_dict,latlon_df)
            return True
        except BaseException as er3:
            return False
            
            
    ec_test(self,fpaths,fextensions)
    
    if not ec_test:
        return False
        
    else:
        kmz_test_extract = EXTRACTION(fpaths,fextensions)
        self.mgrs_dict = kmz_test_extract.mgrs_dict
         
        kmz_test_convert = CONVERSION(self.mgrs_dict)
        self.latlon_dict = kmz_test_convert.latlon_dict
        self.latlon_df = kmz_test_convert.latlon_df
         
        kmz_test(self,self.latlon_dict,self.latlon_df)
         
        if kmz_test:
            return True
        else:
            return False
                        
