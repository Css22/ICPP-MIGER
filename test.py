# import grpc
# import grpc
# import grpc_tool.server_scherduler_pb2_grpc as server_scherduler_pb2_grpc
# import grpc_tool.server_scherduler_pb2 as  server_scherduler_pb2 
# from concurrent import futures


# with grpc.insecure_channel('localhost:50052') as channel:
#     stub = server_scherduler_pb2_grpc.SchedulerServiceStub(channel)

#     job_information = stub.JobState(server_scherduler_pb2.JobStateMessage (
#         type = 'finish', JobID = 2
#         ))
    
#     print(job_information.response)
        
#     predict = stub.Predictor(server_scherduler_pb2.JobCombine (
#         partition = 32,
#         JobIDs = [1,2,3],
#         MPSPercentage = [33,33,33],
#     ))

#     print(predict)

#     load = stub.Load(server_scherduler_pb2.LoadInformation (
#         partition = [1,3,4,5],
#         load = [11,23.2,33,41],
#     ))

#     print(load)


# with grpc.insecure_channel('localhost:50051') as channel:

#     stub = server_scherduler_pb2_grpc.WorkerServiceStub(channel)

#     job_information = stub.AccpetJob(server_scherduler_pb2.JobInformation (
#         JobID=2
#     ))
    
#     print(job_information.response)
import time
import util.MIG_operator as MIG_operator
import util.MPS_operator as MPS_operator



# MIG_operator.create_ins(gpu=0, ins='1g.10gb')

# # MIG_operator.create_ins(gpu=0, ins='1g.10gb')

MPS_operator.SetPercentage(UUID='MIG-9168fcda-71ba-50e7-aa4c-c7a4a0f3453e', Percentage=50)
MPS_operator.SetPercentage(UUID='MIG-f562e13c-35fc-58d3-b3b9-508159b7fbcc', Percentage=50)
# MPS_operator.OpenMPS(UUID='MIG-9168fcda-71ba-50e7-aa4c-c7a4a0f3453e')

# MPS_operator.OpenMPS(UUID='MIG-f562e13c-35fc-58d3-b3b9-508159b7fbcc')


# MPS_operator.CloseMPS(UUID='MIG-9168fcda-71ba-50e7-aa4c-c7a4a0f3453e')
# MPS_operator.CloseMPS(UUID='MIG-f562e13c-35fc-58d3-b3b9-508159b7fbcc')
# MIG_operator.disable_mps()