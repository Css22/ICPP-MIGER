import grpc
import grpc_tool.server_scherduler_pb2_grpc as server_scherduler_pb2_grpc
import grpc_tool.server_scherduler_pb2 as  server_scherduler_pb2 
from concurrent import futures



def WorkerService():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_scherduler_pb2_grpc.add_WorkerServiceServicer_to_server(server_scherduler_pb2_grpc.WorkerServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()



