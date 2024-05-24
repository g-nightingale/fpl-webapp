import boto3

# Create a Lambda client
client = boto3.client('lambda')

def delete_all_lambda_layers():
    # List all layers
    response = client.list_layers()
    layers = response.get('Layers', [])
    
    # Iterate through all layers
    for layer in layers:
        layer_name = layer['LayerName']
        print(f"Deleting all versions of layer {layer_name}")
        
        # List versions of the layer
        version_response = client.list_layer_versions(LayerName=layer_name)
        versions = version_response.get('LayerVersions', [])
        
        # Delete all versions of the layer
        for version in versions:
            version_number = version['Version']
            print(f"Deleting version {version_number} of {layer_name}")
            client.delete_layer_version(LayerName=layer_name, VersionNumber=version_number)

if __name__ == '__main__':
    delete_all_lambda_layers()