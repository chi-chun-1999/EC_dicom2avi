import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.image_process.cycle import ExtractMulitCycle
import pydicom
import re
import time 
import json
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    """ Custom encoder for numpy data types """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):

            return int(obj)

        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)

        elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
            return {'real': obj.real, 'imag': obj.imag}

        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()

        elif isinstance(obj, (np.bool_)):
            return bool(obj)

        elif isinstance(obj, (np.void)): 
            return None

        return json.JSONEncoder.default(self, obj)


def StartExtractData(file_dict:dict,export_path:str,export_data:str,export_whole=True, fps=30):
    """

    The function in the user interface (UI) for extracting data using ExtractMultiCycle.
    
    input: 
    file_dict: the python dictionary the key is file name and the content is ECData
    export_path: the path to store extract data
    export_data: 'all', 'avi', 'npy'
    export_whole: export all dicom array data
    fps: the fps for avi file

    return:
    demc_info: the information for extraction
    
    """

    process_time = time.ctime()
    three_dim_dicom_file = []
    demc_info = {"process_time":process_time,"process_file_num":0,"process_file_info":[]}
    fps = 30
    
    for key, f in file_dict.items():
        extract_multi_cycle = ExtractMulitCycle(f.getPath())
        
        print('=======Process %s======'%(extract_multi_cycle._file_name))

        try:
            extract_multi_cycle.extractCycle()
        except ValueError as err:
            print("Warning:",err)
            three_dim_dicom_file.append(key)
        except pydicom.errors.InvalidDicomError as err:

            print("Error:",'\'%s\' is not dicom file. Please input DICOM file.'%(f))
            return
        
        else:

            if export_data=='all':
                if export_whole:
                    extract_multi_cycle.exportWholeNpy(export_path)
                    extract_multi_cycle.exportWholeAvi(export_path,fps=fps)
                extract_multi_cycle.exportNpy(export_path)
                extract_multi_cycle.exportAvi(export_path,fps=fps)
            elif export_data=='npy':
                if export_whole:
                    extract_multi_cycle.exportWholeNpy(export_path)
                extract_multi_cycle.exportNpy(export_path)
            elif export_data=='avi':
                if export_whole:
                    extract_multi_cycle.exportWholeAvi(export_path,fps=fps)
                extract_multi_cycle.exportAvi(export_path,fps=fps)
            demc_info['process_file_num']+=1
            demc_info['process_file_info'].append(extract_multi_cycle.exportExtractInfo())
        

    if export_path[-1]!='/':
        export_path+='/'
    
    demc_info_file_path =  export_path+'demc_info.json'
    with open(demc_info_file_path, 'w') as f:
      f.write(json.dumps(demc_info, indent = 4,cls=NumpyEncoder))
    
    return demc_info,three_dim_dicom_file
    

    