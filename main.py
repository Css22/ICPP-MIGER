# import MIG_util.get_uuid
import sys
sys.path.append('/data/zbw/MIG/MIG/ATC-MIG')
import MIG_util.MIG_operator as MIG_operator
import grpc_tool.grpc_pb2, grpc_tool.grpc_pb2_grpc
import node.GPU_worker as GPU_worker
import node.Scheduler as  Scheduler
import argparse
# import MIG_util.node_state




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='simulator')
    parser.add_argument('--type', choices=['worker','scheduler'], default='worker')

    args = parser.parse_args()


    if args.type == 'worker':
        GPU_worker.client()
    if args.type == 'scheduler':
        Scheduler.server()