import util.MIG_operator as MIG_operator
import util.MPS_operator as MPS_operator

UUID_list = MIG_operator.get_uuid(0)


for i in UUID_list:
    MPS_operator.CloseMPS(i)

MIG_operator.reset_mig(0)