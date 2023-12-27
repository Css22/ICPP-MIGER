# import MIG_util.get_uuid
import sys
sys.path.append('/data/zbw/MIG/MIG/ATC-MIG')
import util.MIG_operator as MIG_operator
import util.MPS_operator as MPS_operator
import node.GPU_worker as GPU_worker
import node.Scheduler_worker as  Scheduler
import argparse
# import MIG_util.node_state




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='simulator')
    parser.add_argument('--type', choices=['worker','scheduler'], default='worker')

    args = parser.parse_args()


    if args.type == 'worker':
        MIG_operator.reset_mig(0)
        GPU_worker.WorkerService()
    if args.type == 'scheduler':
        Scheduler.start_service()