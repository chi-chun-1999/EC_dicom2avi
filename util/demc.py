import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import glob
import click
#from src.image_process.video import  getRgbArray, array2avi
from src.image_process.cycle import ExtractMulitCycle
import pydicom
import re

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
            if export_data=='all':
                extract_multi_cycle.exportNpy(output)
                extract_multi_cycle.exportAvi(output,fps=fps)
            elif export_data=='npy':
                extract_multi_cycle.exportNpy(output)
            elif export_data=='avi':
                extract_multi_cycle.exportAvi(output,fps=fps)
                
            print()
            
    
    #if len(file_path)==1:
    #    avi_file_search = re.compile(r'avi$')
    #    avi = avi_file_search.search(output)
    #    if avi==None:
    #        raise ValueError('The name of output file must be xxx.avi')
    #    else:
    #        head, tail = os.path.split(output)
    #        if not(os.path.isdir(head)) and head!='':
    #            raise ValueError('The output directory not found!')
    #        output_file = [output]
    #        
    #    
    #
    #elif len(file_path)>=2:
    #    output_file=[]
    #    for f in file_path:
    #        head,tail= os.path.split(f)
    #        if output=='output.avi':
    #            output_file.append('./output_video/'+tail+'.avi')
    #        else:
    #            if os.path.isdir(output):
    #                if output[-1]!='/':
    #                    output_file.append(output+'/'+tail+'.avi')
    #                else:
    #                    output_file.append(output+tail+'.avi')
    #                    
    #            else:
    #                raise FileNotFoundError('Output Directory Not Found!')

    ##print(file_path)
    #for i,f in enumerate(file_path):
    #    dcm = pydicom.dcmread(f)
    #    #rgb_array = getRgbArray(dcm)
    #    #print(rgb_array.shape)
    #    
    #    if only4d==False:
    #        if len(rgb_array.shape)!=4:
    #            raise ValueError('The shape of array data not match. If you want to output only 4D array please add \'--only4d\'')
    #        #array2avi(rgb_array[:,:,:,::-1],output_file[i],fps,fourcc)
    #        print('Finish processing',f)

    #    elif only4d==True:
    #        print('====Output Only 4D array Mode==== ')
    #        if len(rgb_array.shape)==4:
    #            #array2avi(rgb_array[:,:,:,::-1],output_file[i],fps,fourcc)
    #            print('Finish processing',f)


if __name__ == '__main__':
    main()
