import json

GI_ID_table_path = './configs/GI_ID_table.json'

with open(GI_ID_table_path, 'r') as file:
    GI_ID_table = json.load(file)



def map_GI_ID_partition(GI_ID):

    for i in GI_ID_table.keys():
        if GI_ID == 1:
            return '4g.40gb'
        if GI_ID in GI_ID_table[i]:
            return i
