from train import train_model

def lambda_handler(event, context):
    train_model()