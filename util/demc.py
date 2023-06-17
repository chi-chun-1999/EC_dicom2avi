import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import glob
import click
#from src.image_process.video import  getRgbArray, array2avi
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




@click.command()
@click.argument('file_path',nargs=-1,type=click.Path(exists=True))
@click.option('-f','--fps','fps',default=30,help='The fps of avi',type=float,show_default=True)
@click.option('-o','--output','output',default='./',show_default=True,help='The output directory of multi cycle data',type=click.Path())
@click.option('--export_data','export_data',default='all',show_default=True,help='You can only output npy file or avi file. The default will export above of all.',type=str)
def main(file_path,output,fps,export_data):
    #print(file_path,output)
    #click.echo(file_path)
    
    if export_data!='all' and export_data!='npy' and export_data!='avi':
        print("Error: The option of \'--export_data\' must be \'all\', \'npy\' or \'avi\'")
        return 

    process_time = time.ctime()
    demc_info = {"process_time":process_time,"process_file_num":0,"process_file_info":[]}
    
    for f in file_path:

        extract_multi_cycle = ExtractMulitCycle(f)
        print('=======Process %s======'%(extract_multi_cycle._file_name))

        try:
            extract_multi_cycle.extractCycle()
        except ValueError as err:
            print("Warning:",err)
        except pydicom.errors.InvalidDicomError as err:

            print("Error:",'\'%s\' is not dicom file. Please input DICOM file.'%(f))
            return

        else:

            #if export_data=='all':
            #    extract_multi_cycle.exportNpy(output)
            #    extract_multi_cycle.exportAvi(output,fps=fps)
            #elif export_data=='npy':
            #    extract_multi_cycle.exportNpy(output)
            #elif export_data=='avi':
            #    extract_multi_cycle.exportAvi(output,fps=fps)
            demc_info['process_file_num']+=1
            demc_info['process_file_info'].append(extract_multi_cycle.exportExtractInfo())
                
    print(demc_info)
    
    if output[-1]!='/':
        output+='/'
    
    demc_info_file_path =  output+'demc_info.json'
    with open(demc_info_file_path, 'w') as f:
      f.write(json.dumps(demc_info, indent = 4,cls=NumpyEncoder))
    


if __name__ == '__main__':
    main()
