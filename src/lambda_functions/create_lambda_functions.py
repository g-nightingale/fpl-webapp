from package_lambda import package_lambda
import json

CONFIG_FILE = 'config.json'

def main():
    with open(CONFIG_FILE, 'r') as file:
        data = json.load(file)

    for lambda_id, lambda_config in data.items():
        print(f'Packaging lambda function for {lambda_id}')
        function_file=lambda_config['function_file']
        requirements_file=lambda_config['requirements_file']
        output_zip_file=lambda_config['output_zip_file']
        helper_files=lambda_config['helper_files']
        
        package_lambda(
            function_file=function_file,
            requirements_file=requirements_file,
            output_zip_file=output_zip_file,
            helper_files=helper_files
        )

if __name__ == '__main__':
    main()

