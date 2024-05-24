import os
import shutil
import subprocess
import tempfile

def package_lambda(function_file, output_zip_file, requirements_file=None, helper_files=[]):
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Install packages from requirements.txt into the temp directory
        if requirements_file and os.path.exists(requirements_file):
            subprocess.check_call([
                'pip', 'install',
                '-r', requirements_file,
                '--target', tmpdirname
            ])
        
        # Copy the Lambda function code to the temp directory
        shutil.copy(function_file, tmpdirname)

        # Copy helper files
        for helper_file in helper_files:
            shutil.copy(helper_file, tmpdirname)

        # Zip the contents of the temp directory
        shutil.make_archive(base_name=output_zip_file, format='zip', root_dir=tmpdirname)

# Example usage
if __name__ == '__main__':
    package_lambda(
        function_file='lambda_function.py',
        requirements_file='requirements.txt',
        output_zip_file='lambda_function'
    )
