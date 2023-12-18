import sys
import torch
import time
import pandas as pd 
import numpy as np
sys.path.append('/data/zbw/MIG/MIG/MIG_Schedule')
import argparse
from jobs.online.bert import BertModel
from jobs.online.alexnet import alexnet
from jobs.online.open_unmix import open_unmix
from jobs.online.mobilenet_v2 import mobilenet
from jobs.online.deeplabv3 import deeplabv3
from jobs.online.unet import unet
from jobs.online.vgg_splited import vgg16, vgg19
from jobs.online.resnet import resnet50,resnet101,resnet152
from jobs.online.inception_ve import inception_v3

flag_path = "/data/zbw/MIG/MIG/MIG_Schedule/flag"
model_list = {
    "resnet50": resnet50,
    "resnet101": resnet101,
    "resnet152": resnet152,
    "vgg19": vgg19,
    "vgg16": vgg16,
    "inception_v3": inception_v3,
    'unet': unet,
    'deeplabv3':deeplabv3,
    'mobilenet_v2': mobilenet,
    # 'open_unmix':open_unmix,
    'alexnet': alexnet,
    'bert': BertModel,
}

input_list = {
    "resnet50": [3, 244, 244],
    "resnet101": [3, 244, 244],
    "resnet152": [3, 244, 244],
    "vgg19": [3, 244, 244],
    "vgg16": [3, 244, 244],
    "inception_v3": [3, 299, 299],
    "unet": [3,256,256],
    'deeplabv3': [3,256,256],
    'mobilenet_v2': [3,244,244],
    # 'open_unmix': [2,100000],
    'alexnet': [3,244,244],
    'bert': [1024,768],
}

def get_model(model_name):
    return  model_list.get(model_name)

def get_input(model_name, k):
    input = input_list.get(model_name)
    if model_name == 'bert':
        input = torch.LongTensor(np.random.rand(k, 1024, 768)).half().cuda(0)
        masks =  torch.LongTensor(np.zeros((k, 1, 1, 1024))).half().cuda(0)
        return input,masks
    if len(input) == 3:
        return torch.randn(k, input[0], input[1], input[2]).cuda(0)
    else:
        return torch.randn(k, input[0], input[1]).cuda(0)
    
def modify_first_line(filename, new_content):
    with open(filename, 'r') as f:
        lines = f.readlines()
        f.close()

    # 修改第一行内容
    lines[0] = new_content + '\n'

    with open(filename, 'w') as f:
        f.writelines(lines)
        f.close()

def check_first_line(filename, expected_content):
    with open(filename, 'r') as f:
        first_line = f.readline().strip()  # 读取第一行并删除尾部的换行符
        if first_line == expected_content:
            f.close()
            return True
        else:
            f.close()
            return False 
       
        
def Test_MIG_MPS(task, batch, time1, time2):
    
    t = time.time()
   
    if task == 'bert':  
        model = get_model(task)
        model = model().half().cuda(0).eval()
    else:
        model = get_model(task)
        model = model().cuda(0).eval()

    if task == 'bert':
        input,masks = get_input(task, batch)
    else:
        input = get_input(task, batch)

    flag = True
    result_list = []
    num = 1

    while flag:
        start_time = time.time()
        if task == 'bert':
            output= model.run(input,masks,0,12).cpu()
        elif task == 'deeplabv3':
            output= model(input)['out'].cpu()
        else:
            output=model(input).cpu() 
        end_time = time.time()

        if (time.time() - t >= time1 and time.time() - t <= time2):
            result_list.append(end_time - start_time)
        
        if time.time() - t >= num * 5:
            if check_first_line(flag_path, 'True'):
                modify_first_line(flag_path, 'False')
                Flag = False
                break
            else:
                num = num + 1
    data = pd.Series(result_list)
    data = data.sort_values(ascending=True)
        
    return data.quantile(.95)

def Test_MIG(task, batch):
    if task == 'bert':  
        model = get_model(task)
        model = model().half().cuda(0).eval()
    else:
        model = get_model(task)
        model = model().cuda(0).eval()

    if task == 'bert':
        input,masks = get_input(task, batch)
    else:
        input = get_input(task, batch)

    result_list = []

    for i in range(0, 1000):
        start_time = time.time()
        if task == 'bert':
            output= model.run(input,masks,0,12).cpu()
        elif task == 'deeplabv3':
            output= model(input)['out'].cpu()
        else:
            output=model(input).cpu() 
        end_time = time.time()
        result_list.append(end_time - start_time)
    data = pd.Series(result_list)
    return data.quantile(.95)





# if __name__ == "__main__":
#     path = '/data/zbw/MIG/MIG/MIG_Schedule/jobs/profile/online_profile/'
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--config", type=str)
#     parser.add_argument("--task", type=str)
#     parser.add_argument("--batch", type=int)
#     args = parser.parse_args()
#     config = args.config
#     task = args.task
#     batch = args.batch

#     result = 0
#     path = path + task
#     try:
#         result = Test_MIG(task=task, batch=batch)
#     except Exception as e:
#         result = 'error'

#     with open(path, 'a+') as file:
#         output = config+" " +  task + " " + str(batch) + " " + str(result) +"\n"
#         file.write(output)
#     file.close()

    
if __name__ == "__main__":
    path = "/data/zbw/MIG/MIG/MIG_Schedule/jobs/profile/result/2_copy"
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str)
    parser.add_argument("--percentage1", type=int)
    parser.add_argument("--percentage2", type=int)
    parser.add_argument("--task", type=str)
    parser.add_argument("--task2", type=str)
    parser.add_argument("--batch", type=int)
    parser.add_argument("--time1", type=int)
    parser.add_argument("--time2", type=int)

    args = parser.parse_args()
    config = args.config  
    task = args.task
    task2 = args.task2
    percentage1 = args.percentage1
    percentage2 = args.percentage2
    batch = args.batch
    time1 = args.time1
    time2 = args.time2

    start = time.time()
    result = 0

    try:
       
        result = Test_MIG_MPS(task=task, batch=batch, time1=time1, time2=time2)
    except Exception as e:
        result = 'error'
        num = 1
        flag = True
        while flag:
            if time.time() - start >= num * 2:
                if check_first_line(flag_path, 'True'):
                    modify_first_line(flag_path, 'False')
                    flag = False
                else:
                    num = num + 1
    
    
    with open(path, 'a+') as file:
        output =  "online "+ config+" " +  task + " " + str(batch) + " " + str(percentage1) + " " + task2  +  " "+ str(percentage2) + " " + str(result) +"\n"
        file.write(output)
        file.close()