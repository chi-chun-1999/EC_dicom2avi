import os
import sys

from src.ec_ui.ec_ui_data import ECData
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ec_ui.ec_ui_data import *
from src.exception.value_exception import FileTreeError

from src.file_tree.file_tree import Node,FileTree
from src.file_tree.file_tree import PreOrderIter
# from src.ec_ui.process_ui import NumpyEncoder
import json
import abc
import time

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

class OutcomeTree(object):
    def __init__(self):
        

        self._root = Node('root')
        self._process_file_num = Node('process_file_num',parent=self._root) 
        self._process_time = Node('process_time',parent=self._root)
        self._process_patient_info = Node('process_patient_info',parent=self._root)
    def importFromDict(self,outcome_dict):
# process_file = {'patient_id': '0458924','research_id': 'r12d43d','date_info':'2012-12-18','file_name':'HE4K489Y','R_wave_location': [(98, 52), (175, 52), (259, 52)],'extract_frame': [22, 47, 75],'unregular_rr_interval': False,'export_path':'/home/hello/a'}
        self.setProcessInfo(outcome_dict['process_time'],outcome_dict['process_file_num'])
        for patient in outcome_dict['process_patient_info']:
            import_file = {}

            import_file['patient_id'] = patient['patient_id']
            import_file['research_id'] = patient['research_id']
            
            for date in patient['process_date_info']:
                import_file['date_info'] = date['date']

                for file in date['process_file_info']:
                    import_file['file_name'] = file['file_name']
                    import_file['R_wave_location'] = file['R_wave_location']
                    import_file['extract_frame'] = file['extract_frame']
                    import_file['unregular_rr_interval'] = file['unregular_rr_interval']
                    
                    self.addProcessFile(import_file)

    def setProcessInfo(self,file_num:int,process_time:str):

        self._process_file_num.add_children([Node(file_num)])
        self._process_time.add_children([Node(process_time)])
    
    def addPatient(self,patient_id:str,research_id:str):
        
        patient_search_node = self.searchPatient(research_id) 
        
        if patient_search_node==None:
        
            patient_search_node = Node(research_id)
            
            patient_id_node = Node('patient_id')
            patient_id_node.add_children([Node(patient_id)])
            research_id_node = Node('research_id')
            research_id_node.add_children([Node(research_id)])
            # file_date_search_node = Node('')
            
            patient_search_node.add_children([patient_id_node,research_id_node])
            self._process_patient_info.add_children([patient_search_node])
        return patient_search_node
    
    def addPatientDate(self,patient_id:str,research_id:str,date:str):
        
        patient_search_node = self.addPatient(patient_id,research_id)
        
        patient_file_date_search_node = self.searchPatientFileDate(research_id,date)
        
        if patient_file_date_search_node==None:
            patient_file_date_search_node=Node(date)
            date_node = Node('date')
            date_node.add_children([Node(date)])
            
            patient_file_date_search_node.add_children([date_node])
            patient_search_node.add_children([patient_file_date_search_node])
        
        return patient_file_date_search_node
    
    def addProcessFile(self,process_file:dict):

        patient_file_date_search_node = self.addPatientDate(process_file['patient_id'],process_file['research_id'],process_file['date_info'])
        
        process_file_search_node = self.searchProcessFile(process_file)
        
        if process_file_search_node==None:
            process_file_search_node = Node(process_file['file_name'])
            file_name_node = Node('file_name')
            file_name_node.add_children([Node(process_file['file_name'])])
            R_wave_location_node = Node('R_wave_location')
            R_wave_location_node.add_children([Node(process_file['R_wave_location'])])
            extract_frame_node = Node('extract_frame')
            extract_frame_node.add_children([Node(process_file['extract_frame'])])
            unregular_rr_interval_node = Node('unregular_rr_interval')
            unregular_rr_interval_node.add_children([Node(process_file['unregular_rr_interval'])])
            
            process_file_search_node.add_children([file_name_node,R_wave_location_node,extract_frame_node,unregular_rr_interval_node])
            patient_file_date_search_node.add_children([process_file_search_node])
        
        return patient_file_date_search_node
    def searchPatient(self,research_id:str):
        
        patient_search_node = self._searchChild(self._process_patient_info,research_id)
        
        return patient_search_node

    def searchPatientFileDate(self,research_id:str,date:str):
        
        patient_research_node = self.searchPatient(research_id)
        
        if patient_research_node!=None:
            
            patient_file_date_search_node = self._searchChild(patient_research_node,date)
            
            return patient_file_date_search_node

        
        else:
            return None
        
    def searchProcessFile(self,process_file:dict):
        patient_file_date_search_node = self.searchPatientFileDate(process_file['research_id'],process_file['date_info'])
        
        if patient_file_date_search_node!=None:
            process_file_seach_node = self._searchChild(patient_file_date_search_node,process_file['file_name'])
            
            return process_file_seach_node
        
        else:
            return None
        
    def _searchChild(self,search_node,search_name):
        search_node_children = search_node.children 
        for i in range(len(search_node_children)):
            if search_node_children[i].name == search_name:
                # print(search_name)
                return search_node_children[i]
        
        return None
    
    def showPatient(self):
        for i in self._process_patient_info.children:
            print(i)
    
    def showPatientDate(self,research_id:str):
        patient_search_node = self.searchPatient(research_id)
        if patient_search_node!=None:
            for date_search_node in patient_search_node.children[2:]:
                print(date_search_node)
    
    @property
    def process_time(self):
        return self._process_time.children[0].data

    @property
    def process_file_num(self):
        return self._process_file_num.children[0].data
    
    @process_file_num.setter
    def process_file_num(self,value):
        self._process_file_num.children[0].data = value
    
    @property
    def patient_search_nodes(self):
        return self._process_patient_info.children

def outcome_tree_to_dict(outcome_tree:OutcomeTree):
    extract_info = {}
    extract_info['process_time']=outcome_tree.process_time
    extract_info['process_file_num']=outcome_tree.process_file_num
    extract_info['process_patient_info'] = []
    
    for patient in outcome_tree.patient_search_nodes:
        patient_id = patient.children[0].children[0].data
        research_id = patient.children[1].children[0].data

        per_process_patient_info = {}
        per_process_patient_info[patient.children[0].data]=patient_id
        per_process_patient_info[patient.children[1].data]=research_id
        per_process_patient_info['process_date_info']=[]
        for date in patient.children[2:]:
            per_process_date_info = {}
            date_info = date.children[0].children[0].data
            per_process_date_info[date.children[0].data]=date_info
            per_process_date_info['process_file_info'] = []

            for file in date.children[1:]:
                file_name = file.children[0].children[0].data
                R_wave_location = file.children[1].children[0].data
                extract_frame_node = file.children[2].children[0].data
                unregular_rr_interval = file.children[3].children[0].data

                per_process_file_info = {}
                per_process_file_info[file.children[0].data] = file_name
                per_process_file_info[file.children[1].data] = R_wave_location
                per_process_file_info[file.children[2].data] = extract_frame_node
                per_process_file_info[file.children[3].data] = unregular_rr_interval
                per_process_date_info['process_file_info'].append(per_process_file_info)



            per_process_patient_info['process_date_info'].append(per_process_date_info)
                
        extract_info['process_patient_info'].append(per_process_patient_info)
            
    return extract_info


class ExportDataAbs(abc.ABC):
    def __init__(self,export_root_path) -> None:
        super().__init__()
        self._export_root_path = export_root_path
    
    @abc.abstractmethod
    def to_dict(self):
        pass

    @abc.abstractmethod
    def addProcessFile(self,ec_data:ECData,export_extract_info:dict):
        pass
    

    @abc.abstractmethod
    def ECDataGetExportPath(self, ec_data:ECData,file_name_extension,idx):
        pass
    
    def exportDecmInfo(self):
        demc_info = self.to_dict()

        if self._export_root_path[-1]!='/':
            self._export_root_path+='/'
        
        demc_info_file_path =  self._export_root_path+'demc_info.json'
        with open(demc_info_file_path, 'w') as f:
          f.write(json.dumps(demc_info, indent = 4,cls=NumpyEncoder))
          
        return demc_info


class OutcomeTreeExportData(ExportDataAbs):
    def __init__(self, export_root_path) -> None:
        super().__init__(export_root_path)
        self._outcome_tree = OutcomeTree()
        process_time = time.ctime()

        self._outcome_tree.setProcessInfo(0,process_time)
    
    def to_dict(self):
        demc_info = {}

        demc_info['process_time']=self._outcome_tree.process_time
        demc_info['process_patient_info'] = []
        
        for patient in self._outcome_tree.patient_search_nodes:
            patient_id = patient.children[0].children[0].data
            research_id = patient.children[1].children[0].data

            per_process_patient_info = {}
            per_process_patient_info[patient.children[0].data]=patient_id
            per_process_patient_info[patient.children[1].data]=research_id
            per_process_patient_info['process_date_info']=[]
            for date in patient.children[2:]:
                per_process_date_info = {}
                date_info = date.children[0].children[0].data
                per_process_date_info[date.children[0].data]=date_info
                per_process_date_info['process_file_info'] = []

                for file in date.children[1:]:
                    file_name = file.children[0].children[0].data
                    R_wave_location = file.children[1].children[0].data
                    extract_frame_node = file.children[2].children[0].data
                    unregular_rr_interval = file.children[3].children[0].data

                    per_process_file_info = {}
                    per_process_file_info[file.children[0].data] = file_name
                    per_process_file_info[file.children[1].data] = R_wave_location
                    per_process_file_info[file.children[2].data] = extract_frame_node
                    per_process_file_info[file.children[3].data] = unregular_rr_interval
                    per_process_date_info['process_file_info'].append(per_process_file_info)
                    self._outcome_tree.process_file_num += 1



                per_process_patient_info['process_date_info'].append(per_process_date_info)
                    
            demc_info['process_patient_info'].append(per_process_patient_info)
        demc_info['process_file_num']=self._outcome_tree.process_file_num
                
        return demc_info
    
    def addProcessFile(self,ec_data: ECData, export_extract_info: dict):
        
        process_file = {}
        process_file['patient_id'] = ec_data.patient_id
        process_file['research_id'] = ec_data.research_id
        process_file['date_info'] = ec_data.file_date
        process_file['file_name'] = ec_data.file_name

        process_file['R_wave_location'] = export_extract_info['R_wave_location']
        process_file['extract_frame'] = export_extract_info['extract_frame']
        process_file['unregular_rr_interval'] = export_extract_info['unregular_rr_interval']
        
        self._outcome_tree.addProcessFile(process_file)
    
    def ECDataGetExportPath(self, ec_data:ECData,file_name_extension,idx):
        """
        file_name_extension: 'avi' or 'npy
        idx: means to export which cycle from origin dicom file, when idx=-1 means to export whole file
        
        """
        if self._export_root_path[-1]!='/':
            self._export_root_path+='/'
            
        
        if idx != -1:
            export_dir = "%s%s/%s/"%(self._export_root_path,ec_data.research_id,file_name_extension)
        
        else:
            export_dir = "%s%s/whole_%s/"%(self._export_root_path,ec_data.research_id,file_name_extension)
            
        
        self.createOutputDir(export_dir)
        
        file_name=""
        
        if idx != -1:
            file_name = "%s_%s_%d.%s"%(ec_data.file_date,ec_data.file_name,idx,file_name_extension)
        
        else:
            file_name = "%s_%s_whole.%s"%(ec_data.file_date,ec_data.file_name,file_name_extension)
        
        
        export_path = "%s%s"%(export_dir,file_name)
        
        return export_path
        
        
    
    def createOutputDir(self,export_dir):

        if os.path.isdir(export_dir)==False:
            os.makedirs(export_dir)
        
    
    



