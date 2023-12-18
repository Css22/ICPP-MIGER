import sys
sys.path.append('/data/zbw/MIG/MIG/MIG_Schedule')
from jobs.profile.standardized_throughput import *

throught_list = get_throught_single_list()

config_list = ['1c-7g-80gb', '1c-4g-40gb', '1c-3g-40gb', '1c-2g-20gb', '1c-1g-10gb']
config_map = {
    '1c-7g-80gb':7,
    '1c-4g-40gb':4,
    '1c-3g-40gb':3,
    '1c-2g-20gb':2,
    '1c-1g-10gb':1,
}
job_list = []


for i in throught_list:
    if i[0] not in job_list:
        job_list.append(i[0])

def shown_speedup(model_name):
    model_list = []
    for i in throught_list:
        if i[0] == model_name:
            if i[1] in config_list:
                if i[2] =='error':
                    continue
                model_list.append(i)

    for i in model_list:
        i[1] =  config_map.get(i[1])

    
    model_list.reverse()

    for i in range(0,len(model_list)):
        if i - 1 >= 0:
            resource_up = model_list[i][1] / model_list[i - 1][1]
            speend_up = float(model_list[i][2])/ float(model_list[i - 1][2])
            print(model_list[i], resource_up, speend_up)
        else:
            print(model_list[i])
           


for i in job_list:
    shown_speedup(i)

def get_partion(model_name, speed_up):
    pass
