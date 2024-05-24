import os
import tempfile
import shutil
import requests
import tarfile
import zipfile
import subprocess
import shlex

def pip_install_command(command, target_path=None):
    # Check if the command starts with 'pip install'
    if not command.startswith("pip install"):
        raise ValueError("This function only supports pip install commands.")

    # Split the command into shell-acceptable arguments list
    args = shlex.split(command)

    # If a target path is provided, add the --target option
    if target_path:
        args.extend(['--target', target_path])

    # Execute the command
    try:
        result = subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Installation successful:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error during installation:", e.stderr)
    
def download_and_extract_package(url, extract_to):
    """Download and extract a package from a PyPI url."""
    # Get the last part of the URL, generally the filename
    filename = url.split('/')[-1]

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # Get the package content
        response = requests.get(url)
        response.raise_for_status()
        temp_file.write(response.content)
        temp_file_path = temp_file.name
    
    # Now process the file based on its type
    if filename.endswith('.tar.gz'):
        with tarfile.open(temp_file_path, mode="r:gz") as file:
            file.extractall(path=extract_to)
    elif filename.endswith('.zip'):
        with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif filename.endswith('.whl'):
        # Wheels are essentially zip files so we can extract them directly
        with zipfile.ZipFile(temp_file_path, 'r') as wheel:
            wheel.extractall(extract_to)
    else:
        raise ValueError("Unsupported file format for the package: " + url)
    
    # Clean up the temporary file
    os.remove(temp_file_path)

def clean_directory(directory_path):
    for root, dirs, files in os.walk(directory_path, topdown=False):
        for name in dirs:
            if name.endswith(('dist-info', 'egg-info', 'tests')):
                shutil.rmtree(os.path.join(root, name))

def package_layer(output_zip_file, pypi_files=[], helper_files=[], pip_commands=[]):
    TMP_DIR_PATH = 'python/lib/python3.9/site-packages'
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create the necessary directories
        python_dir_path = os.path.join(tmpdirname, TMP_DIR_PATH)
        os.makedirs(python_dir_path)  # Creates the 'python' directory
        # site_packages_path = os.path.join(python_dir_path, 'lib', f'python{python_version}', 'site-packages')
        # os.makedirs(site_packages_path)  # Create the site-packages directory where libraries will be placed

        print('Installing PyPI whls...')
        # Download and extract each PyPI package
        for url in pypi_files:
            # download_and_extract_package(url, extract_to=site_packages_path)
            download_and_extract_package(url, extract_to=python_dir_path)
            
        print('Copying helper files...')
        # Copy helper files
        for helper_file in helper_files:
            shutil.copy(helper_file, python_dir_path)

        print('Running pip commands...')
        for command in pip_commands:
            # Example usage
            pip_install_command(command, target_path=python_dir_path)

        print('Cleaning up unnecessary files...')
        clean_directory(python_dir_path)

        print(f'Creating zip file: {output_zip_file}...')
        # Zip the contents of the temp directory
        shutil.make_archive(base_name=output_zip_file, format='zip', root_dir=tmpdirname)
        print('Finished!')

# Example usage
if __name__ == '__main__':
    package_layer(
        output_zip_file='lambda_layer',
        pypi_files=[
            'https://files.pythonhosted.org/packages/.../numpy-1.19.2-cp38-cp38-manylinux1_x86_64.whl',
            'https://files.pythonhosted.org/packages/.../pandas-1.1.3-cp38-cp38-manylinux1_x86_64.whl'
        ],
        pip_commands=["pip install psycopg2-binary"],
        helper_files=['path/to/helper_module.py']
    )

