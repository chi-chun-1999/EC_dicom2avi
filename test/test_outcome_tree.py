#%%
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.ec_ui.ec_ui_data import *
from src.exception.value_exception import FileTreeError

from src.file_tree.file_tree import Node,FileTree
from src.file_tree.file_tree import PreOrderIter
from src.ec_ui.export_ui import OutcomeTree,outcome_tree_to_dict
import json
import pandas as pd

    
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
# print(json.dumps(outcome_dict,indent=4))
        

# print('-------------------->')
# print('-------------------->')
# print('-------------------->')
import_outcome_tree = OutcomeTree()

import_outcome_tree.importFromDict(outcome_dict)
# import_outcome_tree._root.show()
import_outcome_dict = outcome_tree_to_dict(import_outcome_tree)
# print(json.dumps(import_outcome_dict,indent=4))

#%%
f = lambda node: node.depth==4
stop = lambda node: node.name=="patient_id" or node.name=="research_id" or node.name == "date"
file_nodes = [i for i in PreOrderIter(outcome_tree._root,filter_=f,stop=stop)]

patient_files = {'patient_id':[],'research_id':[],'date_info':[],'file_name':[],'r_wave_location':[],'extract_frame':[],'unregular_rr_interval':[]}

for fn in file_nodes:

    patient_info_node = fn.parent.parent
    patient_id = patient_info_node.children[0].children[0].data
    research_id = patient_info_node.children[1].children[0].data
    date_info = patient_info_node.children[2].children[0].children[0].data


    file_name = fn.children[0].children[0].data
    r_wave_location = fn.children[1].children[0].data
    extract_frame = fn.children[2].children[0].data
    unregular_rr_interval = fn.children[3].children[0].data
    
# process_file = {'patient_id': '0458924','research_id': 'r12d43d','date_info':'2012-12-18','file_name':'HE4K489Y','R_wave_location': [(98, 52), (175, 52), (259, 52)],'extract_frame': [22, 47, 75],'unregular_rr_interval': False,'export_path':'/home/hello/a'}
    # print(patient_id,research_id,date_info,file_name,r_wave_location,extract_frame,unregular_rr_interval)
    patient_files['patient_id'].append(patient_id)
    patient_files['research_id'].append(research_id)
    patient_files['file_name'].append(file_name)
    patient_files['date_info'].append(date_info)
    patient_files['r_wave_location'].append(r_wave_location)
    patient_files['extract_frame'].append(extract_frame)
    patient_files['unregular_rr_interval'].append(unregular_rr_interval)
    # patient_file = {'patient_id':patient_id,'research_id':research_id,'date_info':date_info,'file_name':file_name,'r_wave_location':r_wave_location,'extract_frame':extract_frame,'unregular_rr_interval':unregular_rr_interval}

df = pd.DataFrame(patient_files)
print(df)
    
# %%