import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from image_process import *


import glob
import click
import re


@click.command()
@click.argument('file_path',nargs=-1,type=click.Path())
@click.option('-f','--fps','fps',default=30,help='The fps of avi',type=float,show_default=True)
@click.option('-o','--output','output',default='output.avi',show_default=True,help='The output name of avi file',type=str)
@click.option('--fourcc','fourcc',default='MJPG',help='The Fourcc \'MJPG\',\'DIVX\',\'XVID\'',type=str,show_default=True)
def main(file_path,output,fps,fourcc):
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
                name=os.path.splitext(tail)[0]+"_cycle"
                output_file.append('./output_video/'+name+'.avi')
            else:
                if os.path.isdir(output):
                    if output[-1]!='/':
                        name=os.path.splitext(tail)[0]+"_cycle"
                        output_file.append(output+'/'+name+'.avi')
                    else:
                        name=os.path.splitext(tail)[0]+"_cycle"
                        output_file.append(output+name+'.avi')
                        
                else:
                    raise FileNotFoundError('Output Directory Not Found!')

    for i,f in enumerate(file_path):
        
        print(output_file[i])
        video_array = avi2array(f)
        #print(video_array.shape)




        ecg_roi =getECGRoi_FixSize(video_array) 

        rr_interval_extractor = RRIntervalExtractor()
        rr_start, rr_end = rr_interval_extractor.process(ecg_roi)

        cycle_start = rr_start - int((rr_end-rr_start)/3)
        cycle_end = rr_end - int((rr_end-rr_start)/3)

        array2avi(video_array[cycle_start:cycle_end],output_file[i],fps,fourcc)

        

if __name__ == '__main__':
    main()
    