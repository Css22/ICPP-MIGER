import util.MIG_operator as MIG_operator
import util.MPS_operator as MPS_operator
num_gpu = 2

for i in range(0, num_gpu):
    UUID_list = MIG_operator.get_uuid(i)


    for j in UUID_list:
        MPS_operator.CloseMPS(j)

    MIG_operator.reset_mig(i)