import json
import socket 
import os


import MIG_util.MIG_operator as MIG_operator


node = socket.gethostname()
with open('./configs/MIG_configurations/partition.json') as f:
    partition_code = json.load(f)


export = {}
export[node] = {}




for gpuid in range(2):
    export[node][f'gpu{gpuid}'] = {}
    for code in partition_code:
        MIG_operator.reset_mig(gpuid)
        export[node][f'gpu{gpuid}'][code] = []
        partition = partition_code[code] # [2,2,2,1]

        for p in partition:
            sliceid = GPU_status.num_to_str[p]
            MIG_operator.create_ins(gpuid, sliceid)
        device_ids = read_cuda_device(gpuid, partition)
        export[node][f'gpu{gpuid}'][code] = device_ids[:]


# with open('mig_device_autogen.json', 'w') as f:
#     json.dump(export, f, indent=4)
