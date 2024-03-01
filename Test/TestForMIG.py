import util.MIG_operator as MIG_operator
import copy

def test_GI_ID_6():
    MIG_operator.create_ins_with_ID(gpu=0, ins='1c-1g-10gb',req_ID=11)
    MIG_operator.create_ins_with_ID(gpu=0, ins='1c-2g-20gb',req_ID=6)


def test_table():
    global_config_list = [[7], [4,3], [4,2,1], [4,1,1,1], [3,3], [3,2,1], [3,1,1,1],[2,2,3], [2,1,1,3], [1,1,2,3], [1,1,1,1,3], [2,2,2,1], [2,1,1,2,1],[1,1,2,2,1],[2,1,1,1,1,1],
                   [1,1,2,1,1,1], [1,1,1,1,2,1], [1,1,1,1,1,1,1]]

    global_choose_list = [{7:[0]}, {4:[1], 3:[2]}, {4:[1], 2:[5], 1:[13]}, {4:[1], 1:[11,12,13]}, {3:[1,2]}, {3:[1], 2:[5], 1:[13]}, {3:[1], 1:[11,12,13]}, {3:[2], 2:[3,4]}, {3:[2], 2:[4], 1:[9,10]}, {3:[2], 2:[4], 1:[7,8]}, 
                      {3:[2], 1:[7,8,9,10]}, {2:[3,4,5], 1:[13]}, {2:[3,5], 1:[9,10,13]}, {2:[4,5], 1:[7,8,13]}, {2:[3], 1:[9,10,11,12,13]}, {2:[4], 1:[7,8,11,12,13]}, {2:[5], 1:[7,8,9,10,13]}, {1:[7,8,9,10,11,12,13]}] 
    

    choose_dir = None

    for i in range(0, len(global_config_list)):
        print("-----------------")
        choose_dir = copy.deepcopy(global_choose_list[i])

        for j in global_choose_list[i]:
            print(j, choose_dir[j])
        
        choose_dir = None

    print(global_choose_list)