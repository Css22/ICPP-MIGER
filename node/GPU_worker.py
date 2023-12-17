# import json
# import socket 
# import subprocess
# import io
# import numpy as np
# import socket

# import MIG_util.MIG_operator as MIG_operator


# node = socket.gethostname()
# with open('./configs/MIG_configurations/GI_ID_table.json') as f:
#     GI_ID_dic = json.load(f)

    
# for i in GI_ID_dic.keys():
#     print(GI_ID_dic[i])
# num_GPUs = 1
# export = {}
# export[node] = {}

 

# print(export)


# # with open('mig_device_autogen.json', 'w') as f:
# #     json.dump(export, f, indent=4)



import grpc
import grpc_tool.grpc_pb2 as grpc_pb2 
import grpc_tool.grpc_pb2_grpc as grpc_pb2_grpc
from concurrent import futures

def client():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_pb2_grpc.add_MyServiceServicer_to_server(grpc_pb2_grpc.MyServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


