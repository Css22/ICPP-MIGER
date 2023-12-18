import sys
sys.path.append('/data/zbw/MIG/MIG/MIG_Schedule')

dir = '/data/zbw/MIG/MIG/MIG_Schedule/jobs/profile/offline_profile/'

# mode_list = ['bert', 'GAN', 'mobilenet', 'resnet50' , 'resnet152', 'SqueezeNet', 'transformer', 'unet', 'vit', 'deeplabv3']
mode_list = ['deeplabv3']
config_list = ['1c-7g-80gb','1c-4g-40gb', '1c-3g-40gb', '1c-2g-20gb', '1c-1g-10gb']


def clean_data(data):
    data_list = []

    for line in data:
        line_list = line.split()
       
        if line_list[0] == 'GPU-I':
            data_list.append(line)
    
    tmp_list = []
    for i in data_list:
        line = i.split()
        if float(line[2]) != 0:
            tmp_list.append(i)
    
    num = len(data_list)
    mean_list = [0] * len(i.split())

    for i in tmp_list:
        line = i.split()
        for j in range(2, len(line)):
            mean_list[j] = mean_list[j] + float(line[j])

    for i in range(2, len(mean_list)):
        mean_list[i] = mean_list[i]/num

    data_list = []

    for i in tmp_list:
        line = i.split()
        flag = True
        for j in range(2, len(line)):
            if float(line[j]) < mean_list[j]:
                flag = False
                break
        if flag:
            data_list.append(i)
    return data_list

def collect_data(config, data, path):
    head_list = ['config', 'GRACT', 'SMACT', 'SMOCC', 'TENSO', 'DRAMA', 'FP64A', 'FP32A' , 'FP16A']
    head = ''
    for i in head_list:
        if i!= 'FP16A':
            head = head + i + " "
        else:
            head = head + i + '\n'
    mean_list = [0] * len(data[0].split())

    for i in data:
        line = i.split()
        for j in range(2, len(line)):
            mean_list[j] = mean_list[j] + float(line[j])

    for i in range(2, len(mean_list)):
        mean_list[i] = mean_list[i]/len(data)    
    
    with open(path, 'a+') as file:
        file.seek(0)  
        first_char = file.read(1) 
        if not first_char:
            file.write(head)  
        else:
            file.seek(0, 2)

        input = config + ' '
        for i in range(2, len(mean_list)):
            if i != len(mean_list) - 1:
                input = input + str(round(mean_list[i], 4)) + ' '
            else:
                input = input + str(round(mean_list[i], 4)) + '\n'
        
        file.write(input)
    file.close()




for model in mode_list:
    file_name = dir + model+'_profile'
    index = -1
    tmp_dic = {}
    for i in config_list:
        tmp_dic[i] = []

    with open(file_name, 'r') as f:
       
        for line in f:
            line = line.strip()
            if line in config_list:
                index = config_list.index(line)
                continue
            if index != -1:
                 tmp_dic[config_list[index]].append(line)
        

        for i in tmp_dic.keys():
            new_data_list = clean_data(tmp_dic[i])
            path = dir + model + "_profile_result"
            collect_data(i,new_data_list, path)
    f.close()






    
