import grpc
import grpc_tool.server_scherduler_pb2_grpc as server_scherduler_pb2_grpc
import grpc_tool.server_scherduler_pb2 as  server_scherduler_pb2 
from concurrent import futures
import node.GPU_worker as GPU_worker
import node.Scheduler_worker as Scheduler_woker
import socket
import threading
import time

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
import subprocess
import threading
import util.MIG_operator as MIG_operator
import util.MPS_operator as MPS_operator
import node.GPU_worker as GPU_worker

# # MPS_operator.CloseMPS('MIG-9168fcda-71ba-50e7-aa4c-c7a4a0f3453e')
# # MPS_operator.CloseMPS('MIG-f562e13c-35fc-58d3-b3b9-508159b7fbcc')





# time.sleep(10)
# GPU_worker.stop_monitor(0, ID_1)
# GPU_worker.stop_monitor(0, ID_2)
# MIG_operator.destroy_ins(0, 2)
# MIG_operator.destroy_ins(0, 5)
# MIG_operator.destroy_ins(0, 13)
# MIG_operator.destroy_ins(0, 10)






# monitor_thread = threading.Thread(target=GPU_worker.GPU_monitor, args=(0, ID_1))
# monitor_thread.start()
# GPU_worker.stop_monitor(0, ID_1)
# MIG_operator.destroy_ins(0, ID_1)
# # GPU_worker.update_uuid(0,ID_1, 'create')

# GPU_worker.update_uuid(0,ID_2, 'create')

# process = subprocess.Popen(['nvidia-smi', '-L'], stdout=subprocess.PIPE, text=True)
# result = subprocess.run(['nvidia-smi', '-L'], stdout=subprocess.PIPE)
# output = result.stdout.decode('utf-8')
# print(output)



# GPU_worker.update_uuid(0,ID_1, 'destroy')
# MIG_operator.destroy_ins(0, ID_2)
# GPU_worker.update_uuid(0,ID_2, 'destroy')
# time.sleep(1)
# ID_1 = MIG_operator.create_ins(0,'1c-2g-20gb')
# MIG_operator.destroy_ins(0, ID_1)

# time.sleep(5)
# ID_1 = MIG_operator.create_ins(0,'1c-2g-20gb')
# ID_1 = MIG_operator.create_ins(0,'1c-1g-10gb')
# MIG_operator.destroy_ins(0, ID_1)
# MIG_operator.destroy_ins(0, 3)
# ID = MIG_operator.create_ins(gpu=0, ins='1c-4g-40gb')

MIG_operator.destroy_ins(0, 7)
MIG_operator.destroy_ins(0, 8)
MIG_operator.destroy_ins(0, 9)
MIG_operator.destroy_ins(0, 10)
MIG_operator.destroy_ins(0, 11)
MIG_operator.destroy_ins(0, 12)
MIG_operator.destroy_ins(0, 13)


# MIG_operator.destroy_ins(0, 7)
# MIG_operator.destroy_ins(0, 8)
# MIG_operator.destroy_ins(0, 9)
# MIG_operator.destroy_ins(0, 10)
# MIG_operator.destroy_ins(0, 11)
# MIG_operator.destroy_ins(0, 12)
# MIG_operator.destroy_ins(0, 13)
# MIG_operator.destroy_ins(0, 2)

# ID_1 = MIG_operator.create_ins(0,'1g.10gb')
# ID_2 = MIG_operator.create_ins(0,'1c-4g-40gb')
# ID_2 = MIG_operator.create_ins(0,'1c-3g-40gb')

# monitor_thread = threading.Thread (target=Scheduler_woker.SchedulerService)
# monitor_thread.start()

# time.sleep(2)
# GPU_worker.regist_worker()
# GPU_worker.start_GPU_monitor(0, ID_1)
# GPU_worker.start_GPU_monitor(0, ID_2)

# time.sleep(100)

# GPU_worker.stop_monitor(0, ID_1)
# GPU_worker.stop_monitor(0, ID_2)
