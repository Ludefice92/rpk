import numpy as np

numsToConvert = list(map(int, input().split()))
nparr = np.array(numsToConvert)
print(f"{np.reshape(nparr,(3,3))}")
