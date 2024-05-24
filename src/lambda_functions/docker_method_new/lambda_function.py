import numpy as np

def lambda_handler(event, context):
    x = np.random.rand()
    print(x)