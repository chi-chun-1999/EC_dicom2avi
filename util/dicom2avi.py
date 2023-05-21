import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import glob
import click
from image_process import  getRgbArray, array2avi
import pydicom
import re


@click.command()
@click.argument('file_path',nargs=-1,type=click.Path())
@click.option('-f','--fps','fps',default=30,help='The fps of avi',type=float,show_default=True)
@click.option('-o','--output','output',default='output.avi',show_default=True,help='The output name of avi file',type=str)
@click.option('--fourcc','fourcc',default='MJPG',help='The Fourcc \'MJPG\',\'DIVX\',\'XVID\'',type=str,show_default=True)
@click.option('--only4d',type=bool,default=False,help='Fource to output only 4D array.')
def main(file_path,output,fps,fourcc,only4d):
    #print(file_path,output,fps)
    #files = [f for f in glob.glob(file_path) if os.path.isfile(f)]
    
    #if len(file_path)!=len(output):
    #    raise ValueError('The output file size not match file path')
    if len(file_path)==1:
        avi_file_search = re.compile(r'avi$')
        avi = avi_file_search.search(output)
        if avi==None:
            raise ValueError('The name of output file must be xxx.avi')
        else:
            head, tail = os.path.split(output)
            if not(os.path.isdir(head)) and head!='':
                raise ValueError('The output directory not found!')
            output_file = [output]
            
        
    
    elif len(file_path)>=2:
        output_file=[]
        for f in file_path:
            head,tail= os.path.split(f)
            if output=='output.avi':
                output_file.append('./output_video/'+tail+'.avi')
            else:
                if os.path.isdir(output):
                    if output[-1]!='/':
                        output_file.append(output+'/'+tail+'.avi')
                    else:
                        output_file.append(output+tail+'.avi')
                        
                else:
                    raise FileNotFoundError('Output Directory Not Found!')

    #print(file_path)
    for i,f in enumerate(file_path):
        dcm = pydicom.dcmread(f)
        rgb_array = getRgbArray(dcm)
        #print(rgb_array.shape)
        
        if only4d==False:
            if len(rgb_array.shape)!=4:
                raise ValueError('The shape of array data not match. If you want to output only 4D array please add \'--only4d\'')
            array2avi(rgb_array[:,:,:,::-1],output_file[i],fps,fourcc)
            print('Finish processing',f)

        elif only4d==True:
            print('====Output Only 4D array Mode==== ')
            if len(rgb_array.shape)==4:
                array2avi(rgb_array[:,:,:,::-1],output_file[i],fps,fourcc)
                print('Finish processing',f)


if __name__ == '__main__':
    main()
