
import sys
sys.path.append('/data/zbw/MIG/MIG/MIG_Schedule')
import argparse
import time
t1 =time.time()
from jobs.offline.GAN import GAN_entry
from jobs.offline.transformer import transformer_entry
from jobs.offline.bert import bert_entry
from jobs.offline.resnet50 import resnet50_entry
from jobs.offline.resnet152 import resnet152_entry
from jobs.offline.mobilenet import mobilenet_entry
from jobs.offline.deeplabv3 import deeplabv3_entry
from jobs.offline.SqueezeNet import SqueezeNet_entry
from jobs.offline.unet import unet_entry
from jobs.offline.vit import vit_entry
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
if __name__ == "__main__":
    path = "/data/zbw/MIG/MIG/MIG_Schedule/jobs/profile/result/2_copy"
    flag_path = "/data/zbw/MIG/MIG/MIG_Schedule/flag"
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str)
    parser.add_argument("--percentage1", type=int)
    parser.add_argument("--percentage2", type=int)
    parser.add_argument("--task", type=str)
    parser.add_argument("--task2", type=str)
    parser.add_argument("--batch", type=int)


    args = parser.parse_args()
    config = args.config  
    task = args.task
    task2 = args.task2
    percentage1 = args.percentage1
    percentage2 = args.percentage2
    batch = args.batch

    start = time.time()
    result = 0

    try:
        result = Test_MIG_MPS(model=task)
        modify_first_line(flag_path, 'True')
    except Exception as e:
        result = 'error'
        modify_first_line(flag_path, 'True')




    with open(path, 'a+') as file:
        output =  "offline "+ config+" " +  task  + " " + str(percentage1) + " " + task2 + " "+ str(batch) +  " "+ str(percentage2) + " " + str(result) +"\n"
        file.write(output)
        file.close()

# # Test_MIG 

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--config", type=str)   
#     parser.add_argument("--model", type=str)


#     args = parser.parse_args()
#     config = args.config  
#     model = args.model
#     entry = model_dic.get(model)


#     result = entry()
#     # try:
#     #     result = entry()
#     # except Exception as e:
#     #     result = 'error'

#     print(result)



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
