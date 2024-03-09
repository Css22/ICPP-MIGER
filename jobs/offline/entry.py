import sys
import os
import argparse
import time
import signal
current_dir = os.path.dirname(os.path.abspath(__file__))
util_dir = os.path.join(current_dir, '../../')
sys.path.append(util_dir)
t1 =time.time()
from GAN import GAN_entry
from transformer import transformer_entry
from bert import bert_entry
from resnet50 import resnet50_entry
from resnet152 import resnet152_entry
from mobilenet import mobilenet_entry
from deeplabv3 import deeplabv3_entry
from SqueezeNet import SqueezeNet_entry
from unet import unet_entry
from vit import vit_entry
from util.sharing import *

jobid = 0
item = []
model_dic = {
    'GAN': GAN_entry,
    'transformer': transformer_entry,
    'bert': bert_entry,
    'resnet50': resnet50_entry,
    'resnet152': resnet152_entry,
    'mobilenet': mobilenet_entry,
    'deeplabv3': deeplabv3_entry,
    'SqueezeNet': SqueezeNet_entry,
    'unet': unet_entry,
    'vit': vit_entry,
}
# path = '/data/zbw/MIG/MIG/MIG_Schedule/jobs/profile/offline_result/'

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--config", type=str)   
#     parser.add_argument("--model", type=str)


#     args = parser.parse_args()
#     config = args.config  
#     model = args.model
#     entry = model_dic.get(model)

#     path = path + model


#     try:
#         result = entry()
#     except Exception as e:
#         result = 'error'

#     with open(path, 'a+') as file:
#         output =  config+ " "  + str(result)+"\n"
#         file.write(output)
#         file.close()

def modify_first_line(filename, new_content):
    with open(filename, 'r') as f:
        lines = f.readlines()
        f.close()

    # 修改第一行内容
    lines[0] = new_content + '\n'

    with open(filename, 'w') as f:
        f.writelines(lines)
        f.close()

def Test_MIG_MPS(model):
    entry = model_dic.get(model)
    result = 0
    result = entry()
    
    return result

def Test_MIG(model):

    entry = model_dic.get(model)
    result = 0
    try:
        result = entry()
    except Exception as e:
        result = 'error'
    
    return result


# Test_MIG_MPS
# if __name__ == "__main__":
#     path = "/data/zbw/MIG/MIG/MIG_Schedule/jobs/profile/result/2_copy"
#     flag_path = "/data/zbw/MIG/MIG/MIG_Schedule/flag"
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--config", type=str)
#     parser.add_argument("--percentage1", type=int)
#     parser.add_argument("--percentage2", type=int)
#     parser.add_argument("--task", type=str)
#     parser.add_argument("--task2", type=str)
#     parser.add_argument("--batch", type=int)


#     args = parser.parse_args()
#     config = args.config  
#     task = args.task
#     task2 = args.task2
#     percentage1 = args.percentage1
#     percentage2 = args.percentage2
#     batch = args.batch

#     start = time.time()
#     result = 0

#     try:
#         result = Test_MIG_MPS(model=task)
#         modify_first_line(flag_path, 'True')
#     except Exception as e:
#         result = 'error'
#         modify_first_line(flag_path, 'True')




#     with open(path, 'a+') as file:
#         output =  "offline "+ config+" " +  task  + " " + str(percentage1) + " " + task2 + " "+ str(batch) +  " "+ str(percentage2) + " " + str(result) +"\n"
#         file.write(output)
#         file.close()

# # Test_MIG 
def signal_handler(sig, frame):
    record_job_progress(jobid=jobid , path=util_dir, progress=item[0])
    sys.exit(143)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=str)
    parser.add_argument("--epoch", type=int)
    parser.add_argument('--jobid', type=int)

    
    args = parser.parse_args()
    jobid = args.jobid
    task = args.task
    epoch = args.epoch
   
    item.append(0)
    signal.signal(signal.SIGTERM, signal_handler)
    if jobid:
        initialize = read_job_progress(jobid=jobid, path=util_dir)
    else:
        initialize = 0
    entry = model_dic.get(task)
    
    # result = entry(epoch)
    result = entry(epoch=epoch, initialize=int(initialize), item = item)
    print(result)
    





# if __name__ == "__main__":
#     path = '/data/zbw/MIG/MIG/MIG_Schedule/jobs/profile/offline_profile/'
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--config", type=str)   
#     parser.add_argument("--model", type=str)

    
#     args = parser.parse_args()
#     config = args.config  
#     model = args.model

#     path = path + model


#     try:
#         result = Test_MIG(model=model)
#     except Exception as e:
#         result = 'error'

    # with open(path, 'a+') as file:
    #     output =  config+ " "  + str(model)+ " " +str(result)+ "\n"
    #     file.write(output)
    # file.close()
