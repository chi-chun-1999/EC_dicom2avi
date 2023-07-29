#%%
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ec_ui.ec_ui_data import *
from src.exception.value_exception import FileTreeError

from src.file_tree.file_tree import Node,FileTree
from src.file_tree.file_tree import PreOrderIter
from src.ec_ui.export_ui import OutcomeTree,outcome_tree_to_dict
import json

    
#%%

process_file = {'patient_id': '0458924','research_id': 'r12d43d','date_info':'2012-12-18','file_name':'HE4K489Y','R_wave_location': [(98, 52), (175, 52), (259, 52)],'extract_frame': [22, 47, 75],'unregular_rr_interval': False,'export_path':'/home/hello/a'}
process2_file1 = {'patient_id': '0458925','research_id': 'r122342','date_info':'2012-12-18','file_name':'HE4K489Y','R_wave_location': [(98, 52), (175, 52), (259, 52)],'extract_frame': [22, 47, 75],'unregular_rr_interval': False,'export_path':'/home/hello/a'}
process2_file2 = {'patient_id': '0458925','research_id': 'r122342','date_info':'2012-12-18','file_name':'HE4K589Y','R_wave_location': [(98, 52), (175, 52), (259, 52)],'extract_frame': [22, 47, 75],'unregular_rr_interval': False,'export_path':'/home/hello/a'}

outcome_tree = OutcomeTree() 
outcome_tree.setProcessInfo(12,'20220203')
# export_tree.addPatient(process_file['patient_id'],process_file['research_id'])
# export_tree.addPatientDate(process2_file1['patient_id'],process2_file1['research_id'],process2_file1['date_info'])
# export_tree.addPatientDate(process2_file2['patient_id'],process2_file2['research_id'],process2_file2['date_info'])
# export_tree.addProcessFile(process_file)
# export_tree.addPatient('0458924','r12d43d')
outcome_tree.addProcessFile(process2_file1)
outcome_tree.addProcessFile(process2_file2)
outcome_tree.addProcessFile(process_file)
# export_tree.addProcessFile(process2_file2)
# export_tree._root.show()
# export_tree.showPatient()
# export_tree.showPatientDate(process2_file1['research_id'])

# print('--->',export_tree.searchPatientFileDate('r12d43d',))

# print(export_tree_to_dict(export_tree))
outcome_dict = outcome_tree_to_dict(outcome_tree)
print(json.dumps(outcome_dict,indent=4))
        

print('-------------------->')
print('-------------------->')
print('-------------------->')
import_outcome_tree = OutcomeTree()

import_outcome_tree.importFromDict(outcome_dict)
# import_outcome_tree._root.show()
import_outcome_dict = outcome_tree_to_dict(import_outcome_tree)
print(json.dumps(import_outcome_dict,indent=4))


