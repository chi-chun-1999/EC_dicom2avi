import sys
import matplotlib
from src.file_tree.file_tree import FileTree
import abc

# For getting processed data from FileTree
class FileProcessDataAbs(abc.ABC):
    def __init__(self) -> None:
        super().__init__()
        self._process_data = {}
    
    @abc.abstractmethod
    def getProcessData(self):
        pass 

class FileTreeProcessData(FileProcessDataAbs):
    def __init__(self,file_tree:FileTree):
        super().__init__()
        self._file_tree = file_tree

    def getProcessData(self):
        file_nodes = self._file_tree.file_nodes
        print(self._file_tree.showRootNode())
        
        for i in file_nodes:
            # print(i.data)
            self._process_data[i.data.file_path] = i.data

        return self._process_data



"""
For getting export data from extract frame

extract_info.json
{
        'process_time': process_time,
        'process_file_num': 0,
        'process_patient_info': 
        [
            {
                'patient_id': '0458924',
                'research_id': 'r12d43d',
                'process_date_info':
                [
                    {
                        'date': '2012-12-18',
                        'process_file_info':
                        [
                            {
                                'file_name': 'HE4K489Y',
                                'R_wave_location': [(98, 52), (175, 52), (259, 52)],
                                'extract_frame': [22, 47, 75],
                                'unregular_rr_interval': False
                            },
                            {
                                'file_name': 'HR4R409Y',
                                'R_wave_location': [(93, 52), (170, 52), (249, 52)],
                                'extract_frame': [24, 48, 72],
                                'unregular_rr_interval': False
                            }
                        ]
                    },
                    {
                        'date': '2012-12-20',
                        'process_file_info':
                        [
                            {
                                'file_name': 'HE4K489Y',
                                'R_wave_location': [(98, 52), (175, 52), (259, 52)],
                                'extract_frame': [22, 47, 75],
                                'unregular_rr_interval': False
                            }
                        ]
                    }
                ]
            },
            {
                'patient_id': '0438524',
                'research_id': 'a14dg3d',
                'process_date_info':
                [
                    {
                        'date': '2012-12-19',
                        'process_file_info':
                        [
                            {
                                'file_name': 'HE4K489Y',
                                'R_wave_location': [(98, 52), (175, 52), (259, 52)],
                                'extract_frame': [22, 47, 75],
                                'unregular_rr_interval': False
                            },
                            {
                                'file_name': 'HR4R409Y',
                                'R_wave_location': [(93, 52), (170, 52), (249, 52)],
                                'extract_frame': [24, 48, 72],
                                'unregular_rr_interval': False
                            }
                        ]
                    }
                ]
            
            }
        ]
}

"""
