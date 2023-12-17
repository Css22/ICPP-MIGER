import grpc
import grpc_tool.grpc_pb2 as grpc_pb2
import grpc_tool.grpc_pb2_grpc as grpc_pb2_grpc
from concurrent import futures

def server():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = grpc_pb2_grpc.MyServiceStub(channel)

        job_information = stub.ServerToClientJobMessage(grpc_pb2.JobMessage(
            type = '1',
            model = '2',
            batch = '3',
            epoch = '4',
            state = '5'
        ))
        
        # response_two = stub.ServerToClientScheduleMessage(grpc_pb2_grpc.ScheduleMessage(

        # ))
        # interaction_response = stub.ClientServerConfigMessage(grpc_pb2_grpc.ConfigMessage(

        # ))

        # 处理响应
        # ...