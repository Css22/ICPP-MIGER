import Test.TestForExecutor as TestForExecutor
import util.MIG_operator as MIG_operator
import util.MPS_operator as MPS_operator
UUID = 'MIG-e806816b-27b9-54dd-87dd-c52b4e695397'
# TestForExecutor.test_main()

print(MPS_operator.GetPercentage(UUID))
MPS_operator.SetPercentage(UUID=UUID, Percentage=70)
# MPS_operator.SetPercentage(30)
# TestForExecutor.destory_MPS('MIG-e806816b-27b9-54dd-87dd-c52b4e695397')
# TestForExecutor.destory_MPS('MIG-e806816b-27b9-54dd-87dd-c52b4e695397')
# MIG_operator.reset_mig(0)